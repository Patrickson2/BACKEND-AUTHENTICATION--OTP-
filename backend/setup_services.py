#!/usr/bin/env python3
"""
Interactive setup script for Gmail SMTP and Twilio SMS services
"""

import os
import sys
from getpass import getpass

def setup_gmail_smtp():
    """Setup Gmail SMTP configuration"""
    print("\n === Gmail SMTP Setup ===")
    print("This will configure email OTP delivery.")
    print("You'll need a Gmail account with 2-factor authentication enabled.\n")
    
    # Get Gmail email
    while True:
        email = input("Enter your Gmail address: ").strip()
        if email and "@" in email and "gmail.com" in email:
            break
        print(" Please enter a valid Gmail address.")

    # Get App Password
    print("\n App Password Instructions:")
    print("1. Go to: https://myaccount.google.com/")
    print("2. Click Security → 2-Step Verification → App passwords")
    print("3. Select 'Mail' and 'Other (Custom name)'")
    print("4. Name it 'OTP System' and generate password")
    print("5. Copy the 16-character password\n")
    
    app_password = getpass("Enter your 16-character App Password: ").strip()
    
    if len(app_password) != 16:
        print(" App password must be exactly 16 characters.")
        return False
    
    # Test Gmail connection
    print("\n Testing Gmail SMTP connection...")
    try:
        from lib.email_service import email_service
        result = email_service.send_otp_email(
            email, 
            "123456", 
            "TestUser"
        )
        if result:
            print(" Gmail SMTP configured successfully!")
            return email, app_password
        else:
            print(" Gmail SMTP test failed. Check your credentials.")
            return False
    except Exception as e:
        print(f" Error testing Gmail: {e}")
        return False

def setup_twilio_sms():
    """Setup Twilio SMS configuration"""
    print("\n📱 === Twilio SMS Setup (Optional) ===")
    print("This will configure SMS OTP delivery.")
    print("You'll need a Twilio account.\n")
    
    setup_twilio = input("Do you want to setup SMS delivery? (y/n): ").lower().strip()
    if setup_twilio != 'y':
        print("⏭  SMS setup skipped.")
        return None, None, None
    
    # Get Twilio credentials
    account_sid = input("Enter your Twilio Account SID: ").strip()
    auth_token = getpass("Enter your Twilio Auth Token: ").strip()
    phone_number = input("Enter your Twilio Phone Number (with +): ").strip()
    
    if not all([account_sid, auth_token, phone_number]):
        print(" All Twilio credentials are required.")
        return False
    
    # Test Twilio connection
    print("\n Testing Twilio SMS connection...")
    try:
        from lib.phone_service import phone_service
        
        # Temporarily set credentials
        os.environ['TWILIO_ACCOUNT_SID'] = account_sid
        os.environ['TWILIO_AUTH_TOKEN'] = auth_token
        os.environ['TWILIO_PHONE_NUMBER'] = phone_number
        
        # Test SMS (this will fail in trial mode, but we can check credentials)
        print("Note: SMS sending requires a paid Twilio account.")
        print("Trial accounts can receive SMS but not send them.")
        
        return account_sid, auth_token, phone_number
        
    except Exception as e:
        print(f" Error testing Twilio: {e}")
        return False

def update_env_file(gmail_config, twilio_config):
    """Update .env file with service configurations"""
    env_file = ".env"
    
    # Read existing .env or create new
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
    else:
        content = "# Environment Variables\n"
    
    # Update Gmail configuration
    if gmail_config:
        email, app_password = gmail_config
        content += f"\n# Gmail Configuration\n"
        content += f"GMAIL_EMAIL={email}\n"
        content += f"GMAIL_APP_PASSWORD={app_password}\n"
    
    # Update Twilio configuration
    if twilio_config and twilio_config[0]:
        account_sid, auth_token, phone_number = twilio_config
        content += f"\n# Twilio Configuration\n"
        content += f"TWILIO_ACCOUNT_SID={account_sid}\n"
        content += f"TWILIO_AUTH_TOKEN={auth_token}\n"
        content += f"TWILIO_PHONE_NUMBER={phone_number}\n"
    
    # Add database configuration
    content += f"\n# Database Configuration\n"
    content += f"DATABASE_URL=sqlite:///./auth_system.db\n"
    
    # Write to .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print(f" Configuration saved to {env_file}")

def main():
    """Main setup function"""
    print(" OTP Authentication System - Service Setup")
    print("=" * 50)
    
    # Setup Gmail SMTP
    gmail_config = setup_gmail_smtp()
    
    # Setup Twilio SMS
    twilio_config = setup_twilio_sms()
    
    # Update .env file
    if gmail_config or twilio_config:
        update_env_file(gmail_config, twilio_config)
        
        print("\n Setup completed successfully!")
        print("\nNext steps:")
        print("1. Restart the backend server: python main.py")
        print("2. Test the complete registration flow")
        print("3. Check your email for OTP codes")
        
        if twilio_config and twilio_config[0]:
            print("4. Upgrade your Twilio account to send SMS")
    else:
        print("\n No services were configured.")
        print("Please try again or check the setup guide.")

if __name__ == "__main__":
    main()
