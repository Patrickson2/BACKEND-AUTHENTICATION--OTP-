#!/usr/bin/env python3
"""
Test CLI Database Connection
"""

import os
import sys

# Change to backend directory to use same database
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

# Import backend modules
from lib.database import SessionLocal, engine
from lib.models import Base, User, OTP, LoginAttempt
from lib.auth import hash_password
from datetime import datetime

def test_database():
    print("Testing CLI Database Connection...")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = SessionLocal()
    
    try:
        # Check existing users
        users = db.query(User).all()
        print(f"Current users in database: {len(users)}")
        for user in users:
            print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")
        
        # Add test user if database is empty
        if len(users) == 0:
            print("Adding test user...")
            test_user = User(
                username="testuser",
                email="test@example.com",
                phone_number="+1234567890",
                password=hash_password("password123"),
                created_at=datetime.now()
            )
            db.add(test_user)
            db.commit()
            print(f"Test user added with ID: {test_user.id}")
        
        # Verify user was added
        users = db.query(User).all()
        print(f"Users after test: {len(users)}")
        for user in users:
            print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}")
            
        print("Database test completed successfully!")
        
    except Exception as e:
        print(f"Database test failed: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
