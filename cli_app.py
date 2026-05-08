#!/usr/bin/env python3
"""
CLI Version of OTP Authentication System
Command-line interface for testing authentication
"""

import os
import sys
import getpass
import random
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import backend modules
from backend.lib.database import SessionLocal
from backend.lib.models import User, OTP, LoginAttempt
from backend.lib.auth import hash_password, check_password
from backend.lib.sendgrid_service import sendgrid_service

class CLIAuthSystem:
    def __init__(self):
        self.db = SessionLocal()
        self.current_user = None
        
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("🔐 OTP AUTHENTICATION SYSTEM - CLI")
        print("="*50)
        print("1. Register New User")
        print("2. Login")
        print("3. Exit")
        print("="*50)
        
    def register_user(self):
        """Register a new user"""
        print("\n📝 USER REGISTRATION")
        print("-"*30)
        
        try:
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            phone_number = input("Phone Number (with +): ").strip()
            password = getpass.getpass("Password: ")
            confirm_password = getpass.getpass("Confirm Password: ")
            
            # Validation
            if not username or not email or not password:
                print("❌ All fields are required!")
                return
                
            if password != confirm_password:
                print("❌ Passwords do not match!")
                return
                
            if len(password) < 6:
                print("❌ Password must be at least 6 characters!")
                return
                
            if "@" not in email:
                print("❌ Invalid email format!")
                return
                
            # Check if user exists
            existing_user = self.db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()
            
            if existing_user:
                print("❌ User with this email or username already exists!")
                return
                
            # Create new user
            hashed_password = hash_password(password)
            new_user = User(
                username=username,
                email=email,
                phone_number=phone_number,
                password=hashed_password,
                created_at=datetime.now()
            )
            
            self.db.add(new_user)
            self.db.commit()
            
            print(f"✅ User '{username}' registered successfully!")
            print(f"📧 Email: {email}")
            print(f"📱 Phone: {phone_number}")
            
        except Exception as e:
            print(f"❌ Registration failed: {str(e)}")
            
    def login(self):
        """Login user and generate OTP"""
        print("\n🔑 USER LOGIN")
        print("-"*20)
        
        try:
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ")
            
            if not email or not password:
                print("❌ Email and password are required!")
                return
                
            # Find user
            user = self.db.query(User).filter(User.email == email).first()
            
            if not user:
                print("❌ User not found!")
                return
                
            # Check password
            if not check_password(password, user.password):
                print("❌ Invalid password!")
                return
                
            print(f"✅ Login successful! Welcome, {user.username}")
            
            # Generate OTP
            otp_code = f"{random.randint(100000, 999999)}"
            
            # Store OTP in database
            new_otp = OTP(
                user_id=user.id,
                code=otp_code,
                created_at=datetime.now(),
                expires_at=datetime.now().replace(minute=datetime.now().minute + 10),
                is_used=False
            )
            
            # Invalidate old OTPs
            old_otps = self.db.query(OTP).filter(
                OTP.user_id == user.id,
                OTP.is_used == False
            ).all()
            
            for old_otp in old_otps:
                old_otp.is_used = True
                
            self.db.add(new_otp)
            self.db.commit()
            
            print(f"\n📧 Sending OTP to {user.email}...")
            
            # Send OTP via SendGrid
            success = sendgrid_service.send_otp_email(user.email, otp_code, user.username)
            
            if success:
                print(f"✅ OTP sent successfully!")
                print(f"🔢 Your OTP code is: {otp_code}")
                print(f"⏰ Valid for 10 minutes")
                
                # Verify OTP
                self.verify_otp(user.id, otp_code)
            else:
                print("❌ Failed to send OTP!")
                
        except Exception as e:
            print(f"❌ Login failed: {str(e)}")
            
    def verify_otp(self, user_id, correct_otp):
        """Verify OTP code"""
        print("\n🔐 OTP VERIFICATION")
        print("-"*25)
        
        try:
            attempts = 3
            while attempts > 0:
                user_input = input(f"Enter OTP (attempts left: {attempts}): ").strip()
                
                if user_input == correct_otp:
                    # Mark OTP as used
                    otp = self.db.query(OTP).filter(
                        OTP.user_id == user_id,
                        OTP.code == correct_otp,
                        OTP.is_used == False
                    ).first()
                    
                    if otp:
                        otp.is_used = True
                        self.db.commit()
                        
                    # Record successful login
                    login_attempt = LoginAttempt(
                        user_id=user_id,
                        successful=True,
                        timestamp=datetime.now()
                    )
                    self.db.add(login_attempt)
                    self.db.commit()
                    
                    print("✅ OTP verified successfully!")
                    print("🎉 Authentication complete!")
                    return
                    
                else:
                    attempts -= 1
                    if attempts > 0:
                        print("❌ Invalid OTP! Try again.")
                    else:
                        print("❌ Too many failed attempts!")
                        
                        # Record failed login
                        login_attempt = LoginAttempt(
                            user_id=user_id,
                            successful=False,
                            timestamp=datetime.now()
                        )
                        self.db.add(login_attempt)
                        self.db.commit()
                        
        except Exception as e:
            print(f"❌ OTP verification failed: {str(e)}")
            
    def show_users(self):
        """Show all users (admin function)"""
        print("\n👥 REGISTERED USERS")
        print("-"*25)
        
        users = self.db.query(User).all()
        
        if not users:
            print("No users found!")
            return
            
        for user in users:
            print(f"👤 {user.username} ({user.email})")
            print(f"   📱 {user.phone_number}")
            print(f"   📅 Created: {user.created_at}")
            print()
            
    def run(self):
        """Main application loop"""
        print("🚀 Starting CLI Authentication System...")
        
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("👋 Goodbye!")
                break
            elif choice == "admin":
                # Hidden admin menu
                self.show_users()
            else:
                print("❌ Invalid choice! Please try again.")
                
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = CLIAuthSystem()
    app.run()
