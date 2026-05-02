# 🔐 OTP Authentication System - Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.8+ installed
- Node.js 18+ installed
- A Gmail account (for email OTP)
- A Twilio account (for SMS OTP - optional)

## 🚀 Quick Start

```bash
# 1. Clone and navigate to project
git clone <your-repo-url>
cd auth_system

# 2. Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python migrate_database.py  # Fix database schema

# 3. Setup Frontend
cd ../frontend/Login-OTP
npm install

# 4. Start Services
# Terminal 1 (Backend):
cd ../../backend
source venv/bin/activate
python main.py

# Terminal 2 (Frontend):
cd ../frontend/Login-OTP
npm run dev
```

## 📧 Gmail SMTP Setup

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on "Security"
3. Enable "2-Step Verification"

### Step 2: Generate App Password
1. In Google Security settings, click "App passwords"
2. Select "Mail" for the app
3. Select "Other (Custom name)" and name it "OTP System"
4. Click "Generate"
5. Copy the 16-character password (this is your (onog ujxx bkyn dnls))

### Step 3: Configure Environment
Create a `.env` file in the `backend` directory:

```bash
cd backend
cp .env.example .env
```

Edit the `.env` file:
```env
# Gmail Configuration
GMAIL_EMAIL=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password

# Database
DATABASE_URL=sqlite:///./auth_system.db

# Twilio (Optional - for SMS)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
```

### Step 4: Test Email Service
```bash
cd backend
source venv/bin/activate
python -c "
from lib.email_service import email_service
result = email_service.send_otp_email('test@example.com', '123456', 'TestUser')
print('Email service working:', result)
"
```

## 📱 Twilio SMS Setup (Optional)

### Step 1: Create Twilio Account
1. Sign up at [Twilio Console](https://www.twilio.com/console)
2. Verify your email and phone number

### Step 2: Get Twilio Credentials
1. Go to [Twilio Console](https://www.twilio.com/console)
2. Copy your **Account SID** and **Auth Token**
3. Buy a phone number (or use the trial number)

### Step 3: Configure Twilio
Add to your `.env` file:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+1234567890
```

### Step 4: Test SMS Service
```bash
cd backend
source venv/bin/activate
python -c "
from lib.phone_service import phone_service
result = phone_service.send_otp_sms('+1234567890', '123456', 'TestUser')
print('SMS service working:', result)
"
```

## 🧪 Testing the Complete System

### 1. Test Registration
```bash
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "your-email@gmail.com",
    "phone_number": "+254712345678",
    "password": "testpass123"
  }'
```

### 2. Test Login
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@gmail.com",
    "password": "testpass123"
  }'
```

### 3. Test OTP Generation
```bash
curl -X POST http://localhost:8000/api/generate-otp \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "delivery_method": "email"
  }'
```

## 🔧 Troubleshooting

### Gmail Issues
- **"Less secure apps" error**: Use App Password, not your regular password
- **"Authentication failed"**: Check email and app password are correct
- **"SMTP connection error"**: Check internet connection and firewall

### Twilio Issues
- **"Invalid phone number"**: Use E.164 format (+countrycode+number)
- **"Insufficient funds"**: Upgrade from trial account
- **"Permission denied"**: Check Twilio credentials

### General Issues
- **Port already in use**: Kill existing processes: `pkill -f python`
- **Database errors**: Run `python migrate_database.py`
- **CORS errors**: Backend should be running on port 8000

## 🌐 Access Points

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Countries API**: http://localhost:8000/api/countries

## 📊 System Features

✅ **Secure 6-digit OTP generation** (cryptographically secure)
✅ **48+ countries supported** for phone validation
✅ **Real email delivery** via Gmail SMTP
✅ **SMS delivery** via Twilio (optional)
✅ **Phone number validation** using Google's phonenumbers
✅ **Professional UI** with black/white/red theme
✅ **Password visibility toggles**
✅ **Country search and auto-populate**
✅ **Real-time validation**
✅ **CORS protection**
✅ **Database migration support**

## 🚀 Production Deployment

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Environment Variables for Production
```env
# Production settings
ENV=production
DEBUG=false
DATABASE_URL=sqlite:///./data/auth_system.db
GMAIL_EMAIL=your-production-email@gmail.com
GMAIL_APP_PASSWORD=your-production-app-password
TWILIO_ACCOUNT_SID=your-production-sid
TWILIO_AUTH_TOKEN=your-production-token
TWILIO_PHONE_NUMBER=your-production-number
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all environment variables are set
3. Ensure backend and frontend are running
4. Test individual components as shown in testing section

---

**🎉 Your OTP Authentication System is now ready!**
