#!/usr/bin/env python3
"""
Initialize database tables for OTP Authentication System
"""

# Import database and models
from lib.database import Base, engine
from lib.models import User, OTP, LoginAttempt

def init_database():
    """Initialize database tables"""
    print("Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database initialized successfully!")
    print("Tables created:")
    print("  - users")
    print("  - otps") 
    print("  - login_attempts")

if __name__ == "__main__":
    init_database()
