#!/usr/bin/env python3
"""
Setup local environment variables for email service
"""

import os
from pathlib import Path

def setup_local_env():
    """Setup local environment variables"""
    
    # Check if .env file exists
    env_file = Path("backend/.env")
    
    if not env_file.exists():
        print("Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# Gmail Configuration (for real email sending)
GMAIL_EMAIL=patricksonthairu@gmail.com
GMAIL_APP_PASSWORD=onogujxxbkyndnls

# Twilio Configuration (for real SMS sending)
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number

# Database Configuration
DATABASE_URL=sqlite:///./auth_system.db
""")
        print("Created backend/.env file")
    else:
        print(".env file already exists")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv("backend/.env")
    
    # Check if Gmail credentials are set
    gmail_email = os.getenv("GMAIL_EMAIL")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")
    
    print(f"\nEnvironment Variables Status:")
    print(f"GMAIL_EMAIL: {gmail_email}")
    print(f"GMAIL_APP_PASSWORD: {'Set' if gmail_password else 'Not set'}")
    
    if gmail_email and gmail_password:
        print("\nEmail service is configured!")
        print("You can now test the email service locally.")
    else:
        print("\nEmail service is not configured.")
        print("Please update the .env file with your Gmail credentials.")

if __name__ == "__main__":
    setup_local_env()
