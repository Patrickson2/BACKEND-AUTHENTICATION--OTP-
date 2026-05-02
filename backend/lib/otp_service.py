# This file handles OTP (One-Time Password) codes for secure login verification
import random
from datetime import datetime, timedelta
from lib.models import OTP

def generate_otp_code():
    """Create a random 6-digit number for OTP verification"""
    # Generate a random number between 100000 and 999999 (6 digits)
    random_number = random.randint(100000, 999999)
    
    # Convert the number to a string and return it
    return str(random_number)

def create_new_otp(db, user_id):
    """Generate a new OTP code for a specific user"""
    
    # Step 1: Find any old unused OTP codes for this user
    old_otps = db.query(OTP).filter(
        OTP.user_id == user_id,   
         # For this specific user
        OTP.is_used == False      
         # That haven't been used yet
    ).all()
    
    # Step 2: Mark all old OTP codes as used (so they can't be used anymore)
    for old_otp in old_otps:
        old_otp.is_used = True
    
    # Step 3: Generate a new 6-digit OTP code
    code = generate_otp_code()
    
    # Step 4: Set expiration time (10 minutes from now)
    current_time = datetime.now()
    expires_at = current_time + timedelta(minutes=10)
    
    # Step 5: Create a new OTP record in the database
    new_otp = OTP(
        user_id=user_id,           # Which user this OTP belongs to
        code=code,                 # The 6-digit code
        created_at=current_time,   # When it was created
        expires_at=expires_at,     # When it expires (10 minutes later)
        is_used=False              # It hasn't been used yet
    )
    
    # Step 6: Save the new OTP to the database
    db.add(new_otp)   
     # Add to database session
    db.commit()       
     # Save permanently
    
    # Step 7: Return the code so it can be sent to the user
    return code

def verify_otp_code(db, user_id, entered_code):
    """Check if the OTP code entered by the user is correct and valid"""
    
    # Step 1: Find the OTP code in the database
    otp = db.query(OTP).filter(
        OTP.user_id == user_id,    # For this specific user
        OTP.code == entered_code,  # With the code they entered
        OTP.is_used == False       # That hasn't been used yet
    ).first()
    
    # Step 2: Check if OTP exists and is not expired
    if not otp:
        # No matching OTP found
        return False
    
    if otp.is_expired():
        # OTP exists but has expired
        return False
    
    # Step 3: OTP is valid! Mark it as used so it can't be used again
    otp.is_used = True
    db.commit()  # Save the change
    
    # Step 4: Return True to indicate successful verification
    return True

def send_otp_email(email, otp_code):
    """Send OTP code to user's email (simulated - prints to console)"""
    
    # In a real application, this would send an actual email
    # For this demo, we just print it to the console
    
    print(f"\n" + "="*50)
    print(f" EMAIL SENT TO: {email}")
    print(f"Subject: Your Login Verification Code")
    print(f"")
    print(f"Your OTP code is: {otp_code}")
    print(f"This code will expire in 10 minutes.")
    print(f"")
    print(f"Do not share this code with anyone!")
    print("="*50)
    
    # Return True to indicate email was "sent" successfully
    return True