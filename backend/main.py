#!/usr/bin/env python3
"""
FastAPI Backend for OTP Authentication System
Provides REST API endpoints for user registration, login, and OTP verification
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import database and models
from lib.database import Base
from lib.models import User, OTP, LoginAttempt
from lib.auth import hash_password, check_password
from lib.email_service import email_service
from lib.phone_service import phone_service

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth_system.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OTP Authentication API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class OTPSelectionRequest(BaseModel):
    user_id: int
    delivery_method: str  # "email" or "sms"

class OTPVerifyRequest(BaseModel):
    user_id: int
    otp_code: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    phone_number: str | None
    created_at: datetime

    class Config:
        from_attributes = True

# Helper functions
def generate_otp_code():
    """Generate a cryptographically secure 6-digit OTP code"""
    import secrets
    # Generate a secure random number between 100000 and 999999
    return str(secrets.randbelow(900000) + 100000)

def create_new_otp(db, user_id):
    """Generate a new OTP code for a specific user"""
    
    # Invalidate old unused OTPs
    old_otps = db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.is_used == False
    ).all()
    
    for old_otp in old_otps:
        old_otp.is_used = True
    
    # Generate new OTP
    code = generate_otp_code()
    from datetime import timedelta
    expires_at = datetime.now() + timedelta(minutes=10)
    
    new_otp = OTP(
        user_id=user_id,
        code=code,
        created_at=datetime.now(),
        expires_at=expires_at,
        is_used=False
    )
    
    db.add(new_otp)
    db.commit()
    
    return code

# API Endpoints
@app.get("/")
def root():
    return {"message": "OTP Authentication API is running"}

@app.post("/api/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check username
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check email
    existing_email = db.query(User).filter(User.email == request.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Validate username length
    if len(request.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    
    # Validate password length
    if len(request.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Validate phone number
    is_valid_phone, phone_error = phone_service.validate_phone_number(request.phone_number)
    if not is_valid_phone:
        raise HTTPException(status_code=400, detail=phone_error)
    
    # Create user
    hashed_pwd = hash_password(request.password)
    new_user = User(
        username=request.username,
        email=request.email,
        phone_number=request.phone_number,
        password=hashed_pwd,
        created_at=datetime.now()
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "Registration successful", "user_id": new_user.id}

@app.post("/api/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """First step of login - verify credentials, return user info"""
    
    print(f"🔐 Login attempt for email: {request.email}")
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        print(f"❌ User not found: {request.email}")
        raise HTTPException(status_code=401, detail="User not found. Please register first.")
    
    print(f"👤 User found: {user.username} (ID: {user.id})")
    
    # Check password
    if not check_password(request.password, user.password):
        print(f"❌ Password mismatch for user: {user.email}")
        # Record failed attempt
        failed_attempt = LoginAttempt(
            user_id=user.id,
            successful=False,
            timestamp=datetime.now()
        )
        db.add(failed_attempt)
        db.commit()
        raise HTTPException(status_code=401, detail="Invalid password. Please try again.")
    
    print(f"✅ Login successful for: {user.username}")
    
    # Return user info (for OTP selection step)
    return {
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number
    }

@app.post("/api/generate-otp")
def generate_otp(request: OTPSelectionRequest, db: Session = Depends(get_db)):
    """Generate OTP for the user"""
    
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate OTP code
    otp_code = create_new_otp(db, request.user_id)
    
    # Send OTP via selected method
    success = False
    if request.delivery_method == "email":
        success = email_service.send_otp_email(user.email, otp_code, user.username)
    elif request.delivery_method == "sms":
        success = phone_service.send_otp_sms(user.phone_number, otp_code, user.username)
    
    return {
        "delivery_method": request.delivery_method,
        "sent_successfully": success,
        "message": f"OTP sent via {request.delivery_method}"
    }

@app.post("/api/verify-otp")
def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """Verify OTP code"""
    
    otp = db.query(OTP).filter(
        OTP.user_id == request.user_id,
        OTP.code == request.otp_code,
        OTP.is_used == False
    ).first()
    
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid OTP code")
    
    # Check expiration
    if otp.is_expired():
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    # Mark as used
    otp.is_used = True
    db.commit()
    
    # Record successful login
    success_attempt = LoginAttempt(
        user_id=request.user_id,
        successful=True,
        timestamp=datetime.now()
    )
    db.add(success_attempt)
    db.commit()
    
    # Get user info
    user = db.query(User).filter(User.id == request.user_id).first()
    
    return {
        "message": "Login successful",
        "username": user.username
    }

@app.get("/api/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "created_at": user.created_at
    }

@app.get("/api/countries")
def get_countries():
    """Get supported countries for phone numbers"""
    return phone_service.get_country_info()

@app.get("/api/test-services")
def test_services():
    """Test email and SMS services configuration"""
    email_test = email_service.test_connection()
    sms_test = phone_service.test_sms_service()
    
    return {
        "email_service": "configured" if email_test else "not configured",
        "sms_service": "configured" if sms_test else "not configured"
    }

@app.get("/api/debug/users")
def debug_users(db: Session = Depends(get_db)):
    """Debug endpoint to see all users (remove in production)"""
    users = db.query(User).all()
    return {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "created_at": user.created_at,
                "password_hash": user.password[:20] + "..." if user.password else None
            }
            for user in users
        ],
        "total_users": len(users)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
