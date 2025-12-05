# OTP service for email verification
import random
from datetime import datetime, timedelta
from lib.models import OTP

def generate_otp_code():
    """Create a random 6-digit code"""
    return str(random.randint(100000, 999999))

def create_new_otp(db, user_id):
    """Generate new OTP code for user"""
    # Mark old OTPs as used
    old_otps = db.query(OTP).filter(OTP.user_id == user_id, OTP.is_used == False).all()
    for old_otp in old_otps:
        old_otp.is_used = True
    
    # Create new OTP
    code = generate_otp_code()
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

def verify_otp_code(db, user_id, entered_code):
    """Check if OTP code is correct"""
    otp = db.query(OTP).filter(
        OTP.user_id == user_id,
        OTP.code == entered_code,
        OTP.is_used == False
    ).first()
    
    if not otp or otp.is_expired():
        return False
    
    # Mark as used
    otp.is_used = True
    db.commit()
    return True

def send_otp_email(email, otp_code):
    """Send OTP via email (simulated)"""
    print(f"\n" + "="*50)
    print(f" EMAIL SENT TO: {email}")
    print(f"Your OTP code is: {otp_code}")
    print(f"Expires in 10 minutes")
    print("="*50)
    return True