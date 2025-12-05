# This file handles user authentication - registering, logging in, and managing profiles
import bcrypt
from datetime import datetime
from lib.models import User, LoginAttempt

def hash_password(password):
    """Turn a plain text password into a secure encrypted version"""
    # Convert password string to bytes (required for bcrypt)
    password_bytes = password.encode('utf-8')
    
    # Generate a random salt (makes each hash unique)
    salt = bcrypt.gensalt()
    
    # Create the hashed password using bcrypt
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Convert back to string and return
    return hashed.decode('utf-8')

def check_password(password, hashed_password):
    """Check if a plain password matches the hashed version"""
    # Convert both passwords to bytes
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Use bcrypt to compare them securely
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# def register_new_user(db, username, email, password):
#     """Create a new user account in the database"""
    
#     # Step 1: Check if someone already has this username
#     existing_user = db.query(User).filter(User.username == username).first()
#     if existing_user:
#         return None  # Username is taken
    
#     # Step 2: Check if someone already has this email
#     existing_email = db.query(User).filter(User.email == email).first()
#     if existing_email:
#         return None  # Email is taken
    
#     # Step 3: Create the password hash (never store plain passwords!)
#     hashed_password = hash_password(password)
    
#     # Step 4: Create a new user object
#     new_user = User(
#         username=username,
#         email=email,
#         password=hashed_password,  # Store the hashed version
#         created_at=datetime.now()  # Record when account was created
#     )
    
#     # Step 5: Save the new user to the database
#     db.add(new_user)        # Add to database session
#     db.commit()             # Save changes permanently
#     db.refresh(new_user)    # Get the updated user with ID
    
#     return new_user  # Return the new user object

# def login_user(db, email, password):
#     """Check if user's email and password are correct"""
    
#     # Step 1: Find the user by their email address
#     user = db.query(User).filter(User.email == email).first()
    
#     # Step 2: If no user found with this email, login fails
#     if not user:
#         return None
    
#     # Step 3: Check if the password is correct
#     password_is_correct = check_password(password, user.password)
    
#     if not password_is_correct:
#         # Password is wrong - record this failed attempt
#         failed_attempt = LoginAttempt(
#             user_id=user.id,
#             successful=False,  # This login failed
#             timestamp=datetime.now()
#         )
#         db.add(failed_attempt)
#         db.commit()
#         return None  # Login failed
    
#     # Step 4: Password is correct - return the user
#     return user

# def log_successful_login(db, user_id):
#     """Record a successful login in the database"""
    
#     # Create a record of this successful login
#     success_attempt = LoginAttempt(
#         user_id=user_id,
#         successful=True,  # This login succeeded
#         timestamp=datetime.now()
#     )
    
#     # Save it to the database
#     db.add(success_attempt)
#     db.commit()

# def update_user_info(db, user, new_username=None, new_email=None, new_password=None):
#     """Update user's profile information"""
    
#     # Update username if user provided a new one
#     if new_username:
#         # Check if another user already has this username
#         username_taken = db.query(User).filter(
#             User.username == new_username, 
#             User.id != user.id  # Don't check against current user
#         ).first()
        
#         # Only update if username is available
#         if not username_taken:
#             user.username = new_username
    
#     # Update email if user provided a new one
#     if new_email:
#         # Check if another user already has this email
#         email_taken = db.query(User).filter(
#             User.email == new_email, 
#             User.id != user.id  # Don't check against current user
#         ).first()
        
#         # Only update if email is available
#         if not email_taken:
#             user.email = new_email
    
#     # Update password if user provided a new one
#     if new_password:
#         # Hash the new password before storing
#         user.password = hash_password(new_password)
    
#     # Save all changes to the database
#     db.commit()
#     db.refresh(user)  # Get updated user data

# def delete_user_account(db, user):
#     """Completely remove a user account from the database"""
    
#     # Delete the user (this also deletes related OTP codes and login attempts)
#     db.delete(user)
    
#     # Save the changes permanently
#     db.commit()

# def get_user_by_id(db, user_id):
#     """Find a user by their ID number"""
    
#     # Search for user with matching ID
#     user = db.query(User).filter(User.id == user_id).first()
    
#     return user  # Returns user object or None if not found