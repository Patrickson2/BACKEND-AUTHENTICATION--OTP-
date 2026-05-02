#!/usr/bin/env python3
"""
Real Email Service for OTP Authentication
Uses Gmail SMTP to send OTP codes to users
"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

class EmailService:
    def __init__(self):
        # Gmail SMTP configuration
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587  # For TLS
        self.sender_email = os.getenv("GMAIL_EMAIL", "your-email@gmail.com")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD", "your-app-password")
        
    def send_otp_email(self, recipient_email: str, otp_code: str, username: str) -> bool:
        """
        Send OTP code to user's email address
        
        Args:
            recipient_email: User's email address
            otp_code: 6-digit OTP code
            username: User's username for personalization
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"Your OTP Code - {otp_code}"
            message["From"] = self.sender_email
            message["To"] = recipient_email
            
            # HTML email content with better styling
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #000;
                        color: #fff;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #111;
                        border: 2px solid #ff0000;
                        border-radius: 10px;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header {{
                        color: #ff0000;
                        font-size: 24px;
                        margin-bottom: 20px;
                    }}
                    .otp-code {{
                        font-size: 36px;
                        font-weight: bold;
                        color: #ff0000;
                        background-color: #fff;
                        padding: 20px;
                        border-radius: 5px;
                        margin: 20px 0;
                        letter-spacing: 5px;
                    }}
                    .footer {{
                        color: #888;
                        font-size: 12px;
                        margin-top: 30px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header"> Your OTP Verification Code</div>
                    <p>Hello <strong>{username}</strong>,</p>
                    <p>Use the following OTP code to complete your login:</p>
                    <div class="otp-code">{otp_code}</div>
                    <p>This code will expire in <strong>10 minutes</strong>.</p>
                    <p>If you didn't request this code, please ignore this email.</p>
                    <div class="footer">
                        <p>&copy; 2026 Authentication System | Secure Login Portal</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Attach HTML content
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipient_email, message.as_string())
                
            print(f"✅ OTP email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {recipient_email}: {str(e)}")
            # Fallback to console for development
            print(f"\n{'='*50}")
            print(f"  EMAIL SENT TO: {recipient_email}")
            print(f"  YOUR OTP CODE: {otp_code}")
            print(f"  Valid for 10 minutes")
            print(f"{'='*50}\n")
            return False
    
    def test_connection(self) -> bool:
        """Test SMTP connection"""
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
            print("✅ Gmail SMTP connection successful")
            return True
        except Exception as e:
            print(f"❌ Gmail SMTP connection failed: {str(e)}")
            print("📧 Please set up your Gmail App Password:")
            print("1. Enable 2-factor authentication on your Google account")
            print("2. Generate an App Password (Settings → Security → App Passwords)")
            print("3. Set environment variables:")
            print("   export GMAIL_EMAIL='your-email@gmail.com'")
            print("   export GMAIL_APP_PASSWORD='your-app-password'")
            return False

# Global email service instance
email_service = EmailService()
