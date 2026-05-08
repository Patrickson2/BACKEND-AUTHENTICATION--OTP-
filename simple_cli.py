#!/usr/bin/env python3
"""
Simple CLI for testing OTP Authentication
"""

import os
import sys
import getpass
import random
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import database modules
from backend.lib.database import SessionLocal, engine
from backend.lib.models import Base, User, OTP, LoginAttempt
from backend.lib.auth import hash_password, check_password

class SimpleCLI:
    def __init__(self):
        self.current_user = None
        self.db = SessionLocal()
        
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("🔐 OTP AUTHENTICATION SYSTEM - CLI")
        print("="*50)
        print("1. Register New User")
        print("2. Login with OTP")
        print("3. Test SendGrid Email")
        print("4. Exit")
        print("="*50)
        
    def register_user(self):
        """Register a new user"""
        print("\nUSER REGISTRATION")
        print("-"*30)
        
        try:
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            phone_number = input("Phone Number (with +): ").strip()
            password = getpass.getpass("Password: ")
            confirm_password = getpass.getpass("Confirm Password: ")
            
            # Validation
            if not username or not email or not password:
                print("All fields are required!")
                return
                
            if password != confirm_password:
                print("Passwords do not match!")
                return
                
            if len(password) < 6:
                print("Password must be at least 6 characters!")
                return
                
            if "@" not in email:
                print("Invalid email format!")
                return
                
            # Check if user exists in database
            existing_user = self.db.query(User).filter(User.email == email).first()
            if existing_user:
                print("User with this email already exists!")
                return
                
            # Create new user in database
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
            
            print(f"User '{username}' registered successfully!")
            print(f"Email: {email}")
            print(f"Phone: {phone_number}")
            print("User saved to database!")
            
        except Exception as e:
            print(f"Registration failed: {str(e)}")
            
    def login(self):
        """Login user and generate OTP"""
        print("\nUSER LOGIN")
        print("-"*20)
        
        try:
            email = input("Email: ").strip()
            password = getpass.getpass("Password: ")
            
            if not email or not password:
                print("Email and password are required!")
                return
                
            # Find user in database
            user = self.db.query(User).filter(User.email == email).first()
            
            if not user:
                print("User not found!")
                return
                
            # Check password
            if not check_password(password, user.password):
                print("Invalid password!")
                return
                
            print(f"Login successful! Welcome, {user.username}")
            
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
            
            print(f"\nSending OTP to {email}...")
            
            # Send OTP via SendGrid
            try:
                from backend.lib.sendgrid_service import sendgrid_service
                
                success = sendgrid_service.send_otp_email(email, otp_code, user.username)
                
                if success:
                    print("OTP sent successfully!")
                    print(f"Your OTP code is: {otp_code}")
                    print("Valid for 10 minutes")
                    
                    # Verify OTP
                    self.verify_otp(user.id, otp_code)
                else:
                    print("Failed to send OTP!")
                    
            except Exception as e:
                print(f"SendGrid error: {str(e)}")
                print(f"Your OTP code is: {otp_code}")
                print("SendGrid not configured - OTP shown in console")
                
                # Verify OTP
                self.verify_otp(user.id, otp_code)
                
        except Exception as e:
            print(f"Login failed: {str(e)}")
            
    def verify_otp(self, user_id, correct_otp):
        """Verify OTP code"""
        print("\nOTP VERIFICATION")
        print("-"*25)
        
        try:
            attempts = 3
            while attempts > 0:
                user_input = input(f"Enter OTP (attempts left: {attempts}): ").strip()
                
                if user_input == correct_otp:
                    # Mark OTP as used in database
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
                    
                    print("OTP verified successfully!")
                    print("Authentication complete!")
                    return
                    
                else:
                    attempts -= 1
                    if attempts > 0:
                        print("Invalid OTP! Try again.")
                    else:
                        print("Too many failed attempts!")
                        
                        # Record failed login
                        login_attempt = LoginAttempt(
                            user_id=user_id,
                            successful=False,
                            timestamp=datetime.now()
                        )
                        self.db.add(login_attempt)
                        self.db.commit()
                        
        except Exception as e:
            print(f"OTP verification failed: {str(e)}")
            
    def test_sendgrid(self):
        """Test SendGrid email service"""
        print("\n📧 SENDGRID EMAIL TEST")
        print("-"*25)
        
        try:
            email = input("Enter test email: ").strip()
            otp_code = f"{random.randint(100000, 999999)}"
            username = "TestUser"
            
            print(f"📧 Sending test email to {email}...")
            
            from backend.lib.sendgrid_service import sendgrid_service
            
            success = sendgrid_service.send_otp_email(email, otp_code, username)
            
            if success:
                print("✅ Test email sent successfully!")
                print(f"🔢 OTP code used: {otp_code}")
            else:
                print("❌ Failed to send test email!")
                
        except Exception as e:
            print(f"❌ SendGrid test failed: {str(e)}")
            
    def show_users(self):
        """Show all users"""
        print("\nREGISTERED USERS")
        print("-"*25)
        
        users = self.db.query(User).all()
        
        if not users:
            print("No users found!")
            return
            
        for user in users:
            print(f"User: {user.username} ({user.email})")
            print(f"   Phone: {user.phone_number}")
            print(f"   ID: {user.id}")
            print(f"   Created: {user.created_at}")
            print()
            
    def run(self):
        """Main application loop"""
        print("🚀 Starting Simple CLI Authentication System...")
        
        while True:
            self.show_menu()
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self.register_user()
            elif choice == "2":
                self.login()
            elif choice == "3":
                self.test_sendgrid()
            elif choice == "4":
                print("👋 Goodbye!")
                break
            elif choice == "admin":
                # Hidden admin menu
                self.show_users()
            else:
                print("❌ Invalid choice! Please try again.")
                
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = SimpleCLI()
    app.run()
