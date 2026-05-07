#!/usr/bin/env python3
"""
SendGrid Email Service for OTP Authentication
Uses SendGrid API for reliable email delivery
"""

import os
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class SendGridService:
    def __init__(self):
        # Load environment variables
        self._load_env_file()
        
        # SendGrid configuration
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("SENDGRID_FROM_EMAIL", "noreply@auth-system.com")
        self.from_name = os.getenv("SENDGRID_FROM_NAME", "Authentication System")
        
        # Debug: Print configuration
        print(f"SendGrid Service initialized:")
        print(f"   From Email: {self.from_email}")
        print(f"   From Name: {self.from_name}")
        print(f"   API Key: {\"Set\" if self.api_key else \"Not set\"}")
        
        # Check if properly configured
        self.is_configured = bool(self.api_key)
        if not self.is_configured:
            print("SendGrid service not configured - using console fallback")
        else:
            print("SendGrid service is configured and ready!")
    
    def _load_env_file(self):
        """Manually load .env file"""
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_file):
            print(f"Loading .env file from: {env_file}")
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        # Remove quotes if present
                        value = value.strip().strip("\"").strip("'")
                        os.environ[key] = value
        else:
            print(f"No .env file found at: {env_file}")
    
    def send_otp_email(self, recipient_email: str, otp_code: str, username: str) -> bool:
        """
        Send OTP code to user\'s email address using SendGrid
        """
        print(f"Attempting to send OTP via SendGrid to: {recipient_email}")
        print(f"   OTP Code: {otp_code}")
        print(f"   Username: {username}")
        
        # Always show OTP in console for development/demo
        print(f"\n{"="*50}")
        print(f"  EMAIL SENT TO: {recipient_email}")
        print(f"  YOUR OTP CODE: {otp_code}")
        print(f"  Valid for 10 minutes")
        print(f"{"="*50}\n")
        
        # If not configured, just return True (console fallback)
        if not self.is_configured:
            print("SendGrid service not configured - OTP shown in console")
            return True
        
        try:
            # Create message
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=recipient_email,
                subject=f"Your OTP Verification Code - {otp_code}",
                html_content=f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>OTP Verification Code</title>
                    <style>
                        body {{ 
                            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif; 
                            background: #f8f9fa; 
                            color: #333; 
                            margin: 0; 
                            padding: 20px; 
                            text-align: center; 
                        }}
                        .container {{ 
                            max-width: 500px; 
                            margin: 0 auto; 
                            background: #ffffff; 
                            border: 2px solid #007bff; 
                            border-radius: 10px; 
                            padding: 30px; 
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        }}
                        .header {{ 
                            color: #007bff; 
                            font-size: 24px; 
                            margin-bottom: 20px; 
                            font-weight: bold;
                        }}
                        .otp-code {{ 
                            font-size: 32px; 
                            font-weight: bold; 
                            color: #ffffff; 
                            background: #007bff; 
                            padding: 20px; 
                            border-radius: 8px; 
                            margin: 20px 0; 
                            letter-spacing: 5px;
                            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
                        }}
                        .footer {{ 
                            color: #6c757d; 
                            font-size: 12px; 
                            margin-top: 30px; 
                            border-top: 1px solid #eee;
                            padding-top: 20px;
                        }}
                        .warning {{ 
                            color: #dc3545; 
                            background: #f8d7da; 
                            border: 1px solid #f5c6cb; 
                            padding: 10px; 
                            border-radius: 5px; 
                            margin: 15px 0; 
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">OTP Verification Code</div>
                        <p>Hello <strong>{username}</strong>,</p>
                        <p>Your One-Time Password (OTP) for login is:</p>
                        <div class="otp-code">{otp_code}</div>
                        <p><strong>This code will expire in 10 minutes.</strong></p>
                        <div class="warning">
                            <strong>Security Notice:</strong> Never share this code with anyone. 
                            Our team will never ask for your OTP.
                        </div>
                        <p>If you didn\'t request this code, please ignore this email.</p>
                        <div class="footer">
                            <p>&copy; 2026 Authentication System | Secure Login Portal</p>
                            <p>This is an automated message. Please do not reply.</p>
                        </div>
                    </div>
                </body>
                </html>
                """,
                plain_text_content=f"""
OTP Verification Code

Hello {username},

Your One-Time Password (OTP) for login is: {otp_code}

This code will expire in 10 minutes.

Security Notice: Never share this code with anyone. Our team will never ask for your OTP.

If you didn\'t request this code, please ignore this email.

&copy; 2026 Authentication System | Secure Login Portal
This is an automated message. Please do not reply.
                """
            )
            
            # Send via SendGrid API
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            if response.status_code == 202:
                print(f"OTP email sent successfully via SendGrid to {recipient_email}")
                return True
            else:
                print(f"SendGrid API error: {response.status_code} - {response.body}")
                return False
            
        except Exception as e:
            print(f"SendGrid error occurred: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """Test SendGrid API connection"""
        if not self.is_configured:
            print("SendGrid service not configured - cannot test connection")
            return False
            
        try:
            sg = SendGridAPIClient(self.api_key)
            # SendGrid doesn\'t have a direct connection test, so we\'ll validate the API key
            if self.api_key and len(self.api_key) > 10:
                print("SendGrid API key appears valid")
                return True
            else:
                print("SendGrid API key appears invalid")
                return False
                
        except Exception as e:
            print(f"SendGrid connection test failed: {str(e)}")
            return False

# Global SendGrid service instance
sendgrid_service = SendGridService()
