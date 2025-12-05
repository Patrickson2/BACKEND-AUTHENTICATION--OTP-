# This file defines the database tables (called "models") for our authentication system
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from lib.database import Base

class User(Base):
    """This creates the 'users' table to store user account information"""
    
    # Tell SQLAlchemy what to name this table in the database
    __tablename__ = 'users'
    
    # Define the columns (fields) in the users table
    id = Column(Integer, primary_key=True)  # Unique ID number for each user
    username = Column(String(50), unique=True, nullable=False) 
     # Username (must be unique)
    email = Column(String(100), unique=True, nullable=False)   
     # Email (must be unique)
    password = Column(String(255), nullable=False)            
     # Hashed password (never plain text!)
    created_at = Column(DateTime, default=datetime.now)       
     # When account was created
    
    # Connect this table to other tables (relationships)
    # When a user is deleted, also delete their OTP codes and login attempts
    otp_codes = relationship("OTP", back_populates="user", cascade="all, delete-orphan")
    login_attempts = relationship("LoginAttempt", back_populates="user", cascade="all, delete-orphan")

class OTP(Base):
    """This creates the 'otp_codes' table to store one-time password codes"""
    
    # Tell SQLAlchemy what to name this table in the database
    __tablename__ = 'otp_codes'
    
    # Define the columns in the otp_codes table
    id = Column(Integer, primary_key=True)                    
     # Unique ID for each OTP
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  
    # Which user this OTP belongs to
    code = Column(String(6), nullable=False)                 
     # The 6-digit OTP code
    created_at = Column(DateTime, default=datetime.now)      
     # When OTP was created
    expires_at = Column(DateTime, nullable=False)            
     # When OTP expires
    is_used = Column(Boolean, default=False)                 
     # Has this OTP been used already?
    
    # Connect back to the User table
    user = relationship("User", back_populates="otp_codes")
    
    def is_expired(self):
        """Check if this OTP code has expired (past its expiration time)"""
        current_time = datetime.now()
        return current_time > self.expires_at
    
    def is_valid(self):
        """Check if this OTP is still good to use (not used and not expired)"""
        # OTP is valid if it hasn't been used AND hasn't expired
        not_used = not self.is_used
        not_expired = not self.is_expired()
        return not_used and not_expired

class LoginAttempt(Base):
    """This creates the 'login_attempts' table to track all login tries"""
    
    # Tell SQLAlchemy what to name this table in the database
    __tablename__ = 'login_attempts'
    
    # Define the columns in the login_attempts table
    id = Column(Integer, primary_key=True)                     
    # Unique ID for each login attempt
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False) 
     # Which user tried to login
    timestamp = Column(DateTime, default=datetime.now)        
    # When the login attempt happened
    successful = Column(Boolean, default=False)               
    # Did the login succeed? (True/False)
    
    # Connect back to the User table
    user = relationship("User", back_populates="login_attempts")