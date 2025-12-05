# Database tables (models) for our authentication system
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.database import Base

class User(Base):
    """Table to store user information"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # This will store hashed password
    created_at = Column(DateTime, default=datetime.now)
    
    # Connect to other tables
    otp_codes = relationship("OTP", back_populates="user", cascade="all, delete-orphan")
    login_attempts = relationship("LoginAttempt", back_populates="user", cascade="all, delete-orphan")

class OTP(Base):
    """Table to store OTP codes for login verification"""
    __tablename__ = 'otp_codes'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    code = Column(String(6), nullable=False)  # 6-digit OTP code
    created_at = Column(DateTime, default=datetime.now)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)
    
    # Connect back to User table
    user = relationship("User", back_populates="otp_codes")
    
    def is_expired(self):
        """Check if OTP code has expired"""
        return datetime.now() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is still valid (not used and not expired)"""
        return not self.is_used and not self.is_expired()

class LoginAttempt(Base):
    """Table to track login attempts (successful and failed)"""
    __tablename__ = 'login_attempts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.now)
    successful = Column(Boolean, default=False)
    
    # Connect back to User table
    user = relationship("User", back_populates="login_attempts")