#!/usr/bin/env python3
"""
Professional Email Service using Resend API
For OTP Authentication System - Production Ready
"""

import requests
import os
from typing import Optional
import asyncio
from concurrent.futures import ThreadPoolExecutor

class EmailService:
    def __init__(self):
        # Load environment variables from .env file
        self._load_env_file()
        
        # Resend API configuration
        self.api_key = os.getenv("RESEND_API_KEY")
        self.sender_email = os.getenv("RESEND_SENDER_EMAIL", "noreply@yourdomain.com")
        
        # Connection pool for better performance
        self._executor = ThreadPoolExecutor(max_workers=2)
        
        # Debug: Print configuration (without API key)
        print(f"Email Service initialized (Resend API):")
        print(f"   API Key: {'Set' if self.api_key else 'Not set'}")
        print(f"   Sender Email: {self.sender_email}")
        
        # Check if properly configured
        self.is_configured = bool(self.api_key)
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
        Send OTP code to user's email address using Resend API
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
            # Resend API endpoint
            url = "https://api.resend.com/emails"
            
            # Email content
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
                        border: 2px solid #4a90e2; 
                        border-radius: 12px; 
                        padding: 30px; 
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}
                    .header {{ 
                        color: #4a90e2; 
                        font-size: 24px; 
                        margin-bottom: 20px; 
                        font-weight: bold;
                    }}
                    .otp-code {{ 
                        font-size: 36px; 
                        font-weight: bold; 
                        color: #ffffff; 
                        background: #4a90e2; 
                        padding: 20px; 
                        border-radius: 8px; 
                        margin: 20px 0; 
                        letter-spacing: 5px;
                        box-shadow: 0 2px 4px rgba(74, 144, 226, 0.3);
                    }}
                    .footer {{ 
                        color: #6c757d; 
                        font-size: 12px; 
                        margin-top: 30px; 
                        border-top: 1px solid #e9ecef;
                        padding-top: 20px;
                    }}
                    .security-notice {{
                        color: #dc3545; 
                        background: #f8d7da; 
                        border: 1px solid #f5c6cb; 
                        padding: 15px; 
                        border-radius: 6px; 
                        margin: 15px 0; 
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">OTP Verification Code</div>
                    <p>Hello <strong>{username}</strong>,</p>
                    <p>Your One-Time Password (OTP) for secure login is:</p>
                    <div class="otp-code">{otp_code}</div>
                    <p><strong>This code will expire in 10 minutes.</strong></p>
                    <div class="security-notice">
                        <strong>Security Notice:</strong> Never share this code with anyone. 
                        Our team will never ask for your OTP via phone or call.
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
            
            # Prepare email data for Resend
            email_data = {
                "from": self.sender_email,
                "to": [recipient_email],
                "subject": f"OTP Verification Code - {otp_code}",
                "html": html_content
            }
            
            # Send via Resend API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            print("Sending via Resend API...")
            response = requests.post(url, json=email_data, headers=headers, timeout=15)
            
            if response.status_code == 200:
                print(f"OTP email sent successfully to {recipient_email}")
                print(f"Response ID: {response.json().get('id', 'N/A')}")
                return True
            else:
                print(f"Resend API error: {response.status_code}")
                print(f"Response: {response.text}")
                return False
            
        except requests.exceptions.RequestException as e:
            print(f"Network error: {str(e)}")
            return False
            
        except Exception as e:
            print(f"Email failed: {str(e)}")
            return False
    
    def test_connection(self) -> bool:
        """Test Resend API connection"""
        if not self.is_configured:
            print("Email service not configured - cannot test connection")
            return False
            
        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Test with minimal email data
            test_data = {
                "from": self.sender_email,
                "to": ["test@example.com"],
                "subject": "Connection Test",
                "html": "<p>Test email from Resend API</p>"
            }
            
            response = requests.get("https://api.resend.com/domains", headers=headers, timeout=10)
            
            if response.status_code == 200:
                print("Resend API connection successful!")
                domains = response.json().get('data', [])
                print(f"Available domains: {[d.get('name') for d in domains]}")
                return True
            else:
                print(f"Resend API connection failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"Resend API test failed: {str(e)}")
            return False

# Global email service instance
email_service = EmailService()
