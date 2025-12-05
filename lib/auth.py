# Authentication functions - register, login, update profile
import bcrypt
from datetime import datetime
from lib.models import User, LoginAttempt

def hash_password(password):
    """Convert plain password to secure hash"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def check_password(password, hashed_password):
    """Check if password matches the hashed version"""
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def register_new_user(db, username, email, password):
    """Create a new user account"""
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        return None
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        return None
    
    # Create new user with hashed password
    hashed_pwd = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        password=hashed_pwd,
        created_at=datetime.now()
    )
    
    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db, email, password):
    """Check if user login credentials are correct"""
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return None
    
    # Check password
    if not check_password(password, user.password):
        # Log failed login attempt
        failed_attempt = LoginAttempt(
            user_id=user.id,
            successful=False,
            timestamp=datetime.now()
        )
        db.add(failed_attempt)
        db.commit()
        return None
    
    return user

def log_successful_login(db, user_id):
    """Record successful login in database"""
    success_attempt = LoginAttempt(
        user_id=user_id,
        successful=True,
        timestamp=datetime.now()
    )
    db.add(success_attempt)
    db.commit()

def update_user_info(db, user, new_username=None, new_email=None, new_password=None):
    """Update user profile information"""
    # Update username if provided
    if new_username:
        existing = db.query(User).filter(User.username == new_username, User.id != user.id).first()
        if not existing:
            user.username = new_username
    
    # Update email if provided
    if new_email:
        existing = db.query(User).filter(User.email == new_email, User.id != user.id).first()
        if not existing:
            user.email = new_email
    
    # Update password if provided
    if new_password:
        user.password = hash_password(new_password)
    
    # Save changes
    db.commit()
    db.refresh(user)

def delete_user_account(db, user):
    """Delete user account and all related data"""
    db.delete(user)
    db.commit()

def get_user_by_id(db, user_id):
    """Find user by their ID"""
    return db.query(User).filter(User.id == user_id).first()