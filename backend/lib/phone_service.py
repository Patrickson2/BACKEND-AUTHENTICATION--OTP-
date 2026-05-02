#!/usr/bin/env python3
"""
Phone Service for SMS OTP Authentication
Handles phone number validation and SMS sending via Twilio
Uses phonenumbers library for proper international phone number validation
"""

import re
import os
import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat
from typing import Optional, Dict, Any, List, Tuple

class PhoneService:
    def __init__(self):
        # Twilio configuration (for real SMS)
        self.twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID", "")
        self.twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN", "")
        self.twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER", "")
        
        # Supported countries with their codes and names
        self.supported_countries = [
            {'code': 'US', 'phone_code': '+1', 'name': 'United States', 'pattern': 10},
            {'code': 'CA', 'phone_code': '+1', 'name': 'Canada', 'pattern': 10},
            {'code': 'GB', 'phone_code': '+44', 'name': 'United Kingdom', 'pattern': 10},
            {'code': 'KE', 'phone_code': '+254', 'name': 'Kenya', 'pattern': 9},
            {'code': 'TZ', 'phone_code': '+255', 'name': 'Tanzania', 'pattern': 9},
            {'code': 'UG', 'phone_code': '+256', 'name': 'Uganda', 'pattern': 9},
            {'code': 'IN', 'phone_code': '+91', 'name': 'India', 'pattern': 10},
            {'code': 'CN', 'phone_code': '+86', 'name': 'China', 'pattern': 11},
            {'code': 'JP', 'phone_code': '+81', 'name': 'Japan', 'pattern': 10},
            {'code': 'DE', 'phone_code': '+49', 'name': 'Germany', 'pattern': 10},
            {'code': 'FR', 'phone_code': '+33', 'name': 'France', 'pattern': 9},
            {'code': 'ZA', 'phone_code': '+27', 'name': 'South Africa', 'pattern': 9},
            {'code': 'NG', 'phone_code': '+234', 'name': 'Nigeria', 'pattern': 10},
            {'code': 'BR', 'phone_code': '+55', 'name': 'Brazil', 'pattern': 11},
            {'code': 'MX', 'phone_code': '+52', 'name': 'Mexico', 'pattern': 10},
            {'code': 'IT', 'phone_code': '+39', 'name': 'Italy', 'pattern': 10},
            {'code': 'ES', 'phone_code': '+34', 'name': 'Spain', 'pattern': 9},
            {'code': 'NL', 'phone_code': '+31', 'name': 'Netherlands', 'pattern': 9},
            {'code': 'BE', 'phone_code': '+32', 'name': 'Belgium', 'pattern': 9},
            {'code': 'CH', 'phone_code': '+41', 'name': 'Switzerland', 'pattern': 9},
            {'code': 'AT', 'phone_code': '+43', 'name': 'Austria', 'pattern': 10},
            {'code': 'SE', 'phone_code': '+46', 'name': 'Sweden', 'pattern': 9},
            {'code': 'NO', 'phone_code': '+47', 'name': 'Norway', 'pattern': 8},
            {'code': 'DK', 'phone_code': '+45', 'name': 'Denmark', 'pattern': 8},
            {'code': 'FI', 'phone_code': '+358', 'name': 'Finland', 'pattern': 9},
            {'code': 'PL', 'phone_code': '+48', 'name': 'Poland', 'pattern': 9},
            {'code': 'CZ', 'phone_code': '+420', 'name': 'Czech Republic', 'pattern': 9},
            {'code': 'HU', 'phone_code': '+36', 'name': 'Hungary', 'pattern': 9},
            {'code': 'RO', 'phone_code': '+40', 'name': 'Romania', 'pattern': 9},
            {'code': 'GR', 'phone_code': '+30', 'name': 'Greece', 'pattern': 10},
            {'code': 'PT', 'phone_code': '+351', 'name': 'Portugal', 'pattern': 9},
            {'code': 'IE', 'phone_code': '+353', 'name': 'Ireland', 'pattern': 9},
            {'code': 'AU', 'phone_code': '+61', 'name': 'Australia', 'pattern': 9},
            {'code': 'NZ', 'phone_code': '+64', 'name': 'New Zealand', 'pattern': 9},
            {'code': 'SG', 'phone_code': '+65', 'name': 'Singapore', 'pattern': 8},
            {'code': 'MY', 'phone_code': '+60', 'name': 'Malaysia', 'pattern': 9},
            {'code': 'TH', 'phone_code': '+66', 'name': 'Thailand', 'pattern': 9},
            {'code': 'PH', 'phone_code': '+63', 'name': 'Philippines', 'pattern': 10},
            {'code': 'VN', 'phone_code': '+84', 'name': 'Vietnam', 'pattern': 9},
            {'code': 'ID', 'phone_code': '+62', 'name': 'Indonesia', 'pattern': 10},
            {'code': 'HK', 'phone_code': '+852', 'name': 'Hong Kong', 'pattern': 8},
            {'code': 'TW', 'phone_code': '+886', 'name': 'Taiwan', 'pattern': 9},
            {'code': 'KR', 'phone_code': '+82', 'name': 'South Korea', 'pattern': 10},
            {'code': 'RU', 'phone_code': '+7', 'name': 'Russia', 'pattern': 10},
            {'code': 'UA', 'phone_code': '+380', 'name': 'Ukraine', 'pattern': 9},
            {'code': 'IL', 'phone_code': '+972', 'name': 'Israel', 'pattern': 9},
            {'code': 'AE', 'phone_code': '+971', 'name': 'United Arab Emirates', 'pattern': 9},
            {'code': 'SA', 'phone_code': '+966', 'name': 'Saudi Arabia', 'pattern': 9},
            {'code': 'EG', 'phone_code': '+20', 'name': 'Egypt', 'pattern': 10},
            {'code': 'ZA', 'phone_code': '+27', 'name': 'South Africa', 'pattern': 9},
        ]
    
    def validate_phone_number(self, phone_number: str) -> tuple[bool, str]:
        """
        Validate phone number using phonenumbers library
        
        Args:
            phone_number: Full phone number with country code
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not phone_number:
            return False, "Phone number is required"
        
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(phone_number, None)
            
            # Check if the number is possible and valid
            if not phonenumbers.is_possible_number(parsed_number):
                return False, "Phone number format is not possible for the given country"
            
            if not phonenumbers.is_valid_number(parsed_number):
                return False, "Invalid phone number"
            
            # Format to E.164 standard for storage
            formatted_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
            
            return True, ""
            
        except NumberParseException as e:
            if e.error_type == NumberParseException.INVALID_COUNTRY_CODE:
                return False, "Invalid country code"
            elif e.error_type == NumberParseException.NOT_A_NUMBER:
                return False, "The string supplied did not seem to be a phone number"
            elif e.error_type == NumberParseException.TOO_SHORT_NSN:
                return False, "Phone number too short"
            elif e.error_type == NumberParseException.TOO_SHORT_AFTER_IDD:
                return False, "Phone number too short after international dialing code"
            elif e.error_type == NumberParseException.TOO_LONG_NSN:
                return False, "Phone number too long"
            else:
                return False, "Invalid phone number format"
        except Exception as e:
            return False, f"Phone validation error: {str(e)}"
    
    def format_phone_number(self, country_code: str, number: str) -> str:
        """
        Format phone number with country code
        
        Args:
            country_code: Country code (e.g., '+1')
            number: Phone number without country code
            
        Returns:
            str: Formatted full phone number
        """
        # Remove any non-digit characters
        clean_number = re.sub(r'[^\d]', '', number)
        return country_code + clean_number
    
    def get_country_info(self) -> List[Dict[str, Any]]:
        """Get list of supported countries with their codes and details"""
        # Group by phone code to handle shared codes (like US/Canada both +1)
        grouped_countries = {}
        
        for country in self.supported_countries:
            phone_code = country['phone_code']
            if phone_code not in grouped_countries:
                grouped_countries[phone_code] = {
                    'phone_code': phone_code,
                    'countries': [],
                    'pattern': country['pattern']
                }
            grouped_countries[phone_code]['countries'].append({
                'code': country['code'],
                'name': country['name']
            })
        
        # Convert to list format for frontend
        result = []
        for phone_code, info in grouped_countries.items():
            if len(info['countries']) == 1:
                # Single country
                country = info['countries'][0]
                result.append({
                    'code': phone_code,
                    'name': country['name'],
                    'country_code': country['code'],
                    'pattern': f"{info['pattern']} digits"
                })
            else:
                # Multiple countries share same code
                names = [c['name'] for c in info['countries']]
                result.append({
                    'code': phone_code,
                    'name': f"{names[0]}/{names[1]}",  # Show first two countries
                    'country_code': info['countries'][0]['code'],
                    'pattern': f"{info['pattern']} digits",
                    'all_countries': info['countries']
                })
        
        # Sort by phone code
        return sorted(result, key=lambda x: x['code'])
    
    def send_otp_sms(self, phone_number: str, otp_code: str, username: str) -> bool:
        """
        Send OTP code via SMS using Twilio
        
        Args:
            phone_number: Full phone number with country code
            otp_code: 6-digit OTP code
            username: User's username
            
        Returns:
            bool: True if SMS sent successfully, False otherwise
        """
        try:
            # Check if Twilio credentials are configured
            if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
                print("⚠️  Twilio not configured - falling back to console output")
                self._fallback_to_console(phone_number, otp_code, username)
                return False
            
            # Import Twilio only when needed
            from twilio.rest import Client
            
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            
            message = client.messages.create(
                body=f"🔐 {username}, your OTP code is: {otp_code}. Valid for 10 minutes. Do not share this code.",
                from_=self.twilio_phone_number,
                to=phone_number
            )
            
            print(f"✅ SMS sent to {phone_number} (SID: {message.sid})")
            return True
            
        except ImportError:
            print("⚠️  Twilio library not installed - falling back to console output")
            self._fallback_to_console(phone_number, otp_code, username)
            return False
        except Exception as e:
            print(f"❌ Failed to send SMS to {phone_number}: {str(e)}")
            self._fallback_to_console(phone_number, otp_code, username)
            return False
    
    def _fallback_to_console(self, phone_number: str, otp_code: str, username: str):
        """Fallback method for development/testing"""
        print(f"\n{'='*50}")
        print(f"  SMS SENT TO: {phone_number}")
        print(f"  USER: {username}")
        print(f"  YOUR OTP CODE: {otp_code}")
        print(f"  Valid for 10 minutes")
        print(f"{'='*50}\n")
    
    def test_sms_service(self) -> bool:
        """Test SMS service configuration"""
        if not all([self.twilio_account_sid, self.twilio_auth_token, self.twilio_phone_number]):
            print("⚠️  Twilio SMS service not configured")
            print("📱 To enable real SMS:")
            print("1. Sign up for Twilio account")
            print("2. Get a Twilio phone number")
            print("3. Set environment variables:")
            print("   export TWILIO_ACCOUNT_SID='your-account-sid'")
            print("   export TWILIO_AUTH_TOKEN='your-auth-token'")
            print("   export TWILIO_PHONE_NUMBER='your-twilio-number'")
            print("4. Install Twilio library: pip install twilio")
            return False
        
        try:
            from twilio.rest import Client
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            # Test by trying to get account info
            account = client.api.accounts(self.twilio_account_sid).fetch()
            print(f"✅ Twilio SMS service ready (Account: {account.friendly_name})")
            return True
        except Exception as e:
            print(f"❌ Twilio SMS service test failed: {str(e)}")
            return False

# Global phone service instance
phone_service = PhoneService()
