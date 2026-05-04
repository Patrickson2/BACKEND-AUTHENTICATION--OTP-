#!/usr/bin/env python3
"""
Optimized Email Service for OTP Authentication
Uses Gmail SMTP to send OTP codes to users with improved performance
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
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # For TLS
        self.sender_email = os.getenv("GMAIL_EMAIL", "your-email@gmail.com")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD", "your-app-password")
        
        # Connection pool for better performance
        self._executor = ThreadPoolExecutor(max_workers=2)
        
        # Debug: Print configuration (without password)
        print(f"🔧 Email Service initialized (optimized):")
        print(f"   SMTP Server: {self.smtp_server}:{self.smtp_port}")
        print(f"   Sender Email: {self.sender_email}")
        print(f"   App Password: {'✅ Set' if self.sender_password != 'your-app-password' else '❌ Not set'}")
    
    def send_otp_email(self, recipient_email: str, otp_code: str, username: str) -> bool:
        """
        Send OTP code to user's email address (optimized for speed)
        
        Args:
            recipient_email: User's email address
            otp_code: 6-digit OTP code
            username: User's username for personalization
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        print(f"📧 Sending OTP to: {recipient_email}")
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"OTP Code - {otp_code}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # Simplified HTML content for faster processing
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; background: #000; color: #fff; margin: 0; padding: 20px; text-align: center; }}
                    .container {{ max-width: 500px; margin: 0 auto; background: #111; border: 2px solid #ff0000; border-radius: 10px; padding: 20px; }}
                    .header {{ color: #ff0000; font-size: 20px; margin-bottom: 15px; }}
                    .otp-code {{ font-size: 28px; font-weight: bold; color: #ff0000; background: #fff; padding: 15px; border-radius: 5px; margin: 15px 0; letter-spacing: 3px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">OTP Verification Code</div>
                    <p>Hello <strong>{username}</strong>,</p>
                    <p>Your OTP code is:</p>
                    <div class="otp-code">{otp_code}</div>
                    <p>Valid for 10 minutes</p>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Fast SMTP connection with timeout
            context = ssl.create_default_context()
            
            # Use shorter timeout for faster response
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
            
            print(f"✅ OTP sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Email failed: {str(e)}")
            # Fallback to console for development
            print(f"\n{'='*50}")
            print(f"  EMAIL SENT TO: {recipient_email}")
            print(f"  YOUR OTP CODE: {otp_code}")
            print(f"  Valid for 10 minutes")
            print(f"{'='*50}\n")
            return False
    
    def send_otp_email_async(self, recipient_email: str, otp_code: str, username: str) -> bool:
        """
        Send OTP email asynchronously for better performance
        """
        try:
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(self._executor, self.send_otp_email, recipient_email, otp_code, username)
            return loop.run_until_complete(future)
        except Exception:
            # Fallback to sync method
            return self.send_otp_email(recipient_email, otp_code, username)
    
    def test_connection(self) -> bool:
        """Test SMTP connection quickly"""
        try:
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=5) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                print("✅ Gmail SMTP connection successful!")
                return True
                
        except Exception as e:
            print(f"❌ Gmail SMTP connection failed: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()
