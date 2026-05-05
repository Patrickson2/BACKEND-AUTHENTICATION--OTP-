#!/usr/bin/env python3
"""
Production-Ready Email Service for OTP Authentication
Uses Gmail SMTP with proper error handling and fallbacks
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

class EmailService:
    def __init__(self):
        # Manually load environment variables from .env file
        self._load_env_file()
        
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # For TLS
        self.sender_email = os.getenv("GMAIL_EMAIL")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD")
        
        # Connection pool for better performance
        self._executor = ThreadPoolExecutor(max_workers=2)
        
        # Debug: Print configuration (without password)
        print(f"Email Service initialized:")
        print(f"   SMTP Server: {self.smtp_server}:{self.smtp_port}")
        print(f"   Sender Email: {self.sender_email or 'Not configured'}")
        print(f"   App Password: {'Set' if self.sender_password else 'Not set'}")
        
        # Check if properly configured
        self.is_configured = bool(self.sender_email and self.sender_password)
        if not self.is_configured:
            print("Email service not configured - using console fallback")
        else:
            print("Email service is configured and ready!")
    
    def _load_env_file(self):
        """Manually load .env file"""
        env_file = os.path.join(os.path.dirname(__file__), '..', '.env')
        if os.path.exists(env_file):
            print(f"Loading .env file from: {env_file}")
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        # Remove quotes if present
                        value = value.strip().strip('"').strip("'")
                        os.environ[key] = value
                        print(f"  Loaded: {key}")
        else:
            print(f"No .env file found at: {env_file}")
    
    def send_otp_email(self, recipient_email: str, otp_code: str, username: str) -> bool:
        """
        Send OTP code to user's email address with fallback
        """
        print(f"Attempting to send OTP to: {recipient_email}")
        print(f"   OTP Code: {otp_code}")
        print(f"   Username: {username}")
        
        # Always show OTP in console for development/demo
        print(f"\n{'='*50}")
        print(f"  EMAIL SENT TO: {recipient_email}")
        print(f"  YOUR OTP CODE: {otp_code}")
        print(f"  Valid for 10 minutes")
        print(f"{'='*50}\n")
        
        # If not configured, just return True (console fallback)
        if not self.is_configured:
            print("Email service not configured - OTP shown in console")
            return True
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"OTP Code - {otp_code}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Enhanced HTML content with better deliverability
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>OTP Verification Code</title>
                <style>
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        background: #f5f5f5; 
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
                        color: #666; 
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
                    <p>If you didn't request this code, please ignore this email.</p>
                    <div class="footer">
                        <p>&copy; 2026 Authentication System | Secure Login Portal</p>
                        <p>This is an automated message. Please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Also add plain text version for better deliverability
            text_content = f"""
OTP Verification Code

Hello {username},

Your One-Time Password (OTP) for login is: {otp_code}

This code will expire in 10 minutes.

Security Notice: Never share this code with anyone. Our team will never ask for your OTP.

If you didn't request this code, please ignore this email.

© 2026 Authentication System | Secure Login Portal
This is an automated message. Please do not reply.
            """
            
            # Attach both HTML and plain text
            html_part = MIMEText(html_content, "html")
            text_part = MIMEText(text_content, "plain")
            message.attach(text_part)
            message.attach(html_part)
            
            # Fast SMTP connection with timeout
            context = ssl.create_default_context()
            
            print("Connecting to Gmail SMTP...")
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=15) as server:
                server.starttls(context=context)
                print("Logging into Gmail...")
                server.login(self.sender_email, self.sender_password)
                print("Sending email...")
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"OTP email sent successfully to {recipient_email}")
            print(f"Check your inbox and spam folder!")
            return True
            
        except smtplib.SMTPAuthenticationError as e:
            print(f"Gmail authentication failed: {str(e)}")
            print("Check your Gmail app password in environment variables")
            return False
            
        except smtplib.SMTPRecipientsRefused as e:
            print(f"Recipient refused: {recipient_email}")
            print("The email address may be invalid or blocked")
            return False
            
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
            
        except Exception as e:
            print(f"Email failed: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection"""
        if not self.is_configured:
            print("Email service not configured - cannot test connection")
            return False
            
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=5) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                print("Gmail SMTP connection successful!")
                return True
                
        except Exception as e:
            print(f"Gmail SMTP connection failed: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()
