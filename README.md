# OTP Authentication System

> A complete authentication system with CLI, Web API, and real OTP delivery via Email/SMS

## System Overview

This project has evolved from a simple CLI authentication system to a full-featured web application with:

- **CLI Interface**: Original command-line authentication (for learning)
- **Web API**: FastAPI backend with REST endpoints
- **React Frontend**: Modern web interface with black/white/red theme
- **Real OTP Delivery**: SendGrid API + Twilio SMS integration
- **48+ Countries**: International phone number validation
- **Secure 6-Digit OTP**: Cryptographically secure code generation

## Architecture

```
auth_system/
├── 📁 backend/           # FastAPI Web API
│   ├── main.py          # API endpoints & server
│   ├── lib/             # Core services
│   │   ├── sendgrid_service.py  # SendGrid API
│   │   ├── phone_service.py  # Twilio SMS
│   │   ├── auth.py      # Password hashing
│   │   ├── models.py    # SQLAlchemy models
│   │   └── database.py  # Database connection
│   └── requirements.txt # Python dependencies
├── 📁 frontend/         # React Web App
│   └── Login-OTP/       # TypeScript React app
├── 📁 Dockerfile        # Container configuration
├── 📁 run_local.sh      # Local development script
└── 📁 README.md         # Project documentation
```

## Quick Start Commands

### Option 1: Web Application (Recommended)

````bash
# Backend Setup
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
./setup.sh  # Initialize database and setup
```

### Option 2: SendGrid API Setup (Required for Email OTP)

1. **Create SendGrid Account**:
   - Go to [SendGrid.com](https://sendgrid.com)
   - Sign up for a free account
   - Verify your email address

2. **Generate API Key**:
   - Go to Settings → API Keys
   - Create new API key
   - Copy the API key (starts with `SG.`)

3. **Configure Environment Variables**:
   ```bash
   # Add to backend/.env
   SENDGRID_API_KEY=SG.your_api_key_here
   SENDGRID_FROM_EMAIL=noreply@yourdomain.com
   SENDGRID_FROM_NAME=Your App Name
````

4. **Test SendGrid Service**:
   ```bash
   cd backend
   python3 -c "from lib.sendgrid_service import sendgrid_service; sendgrid_service.test_connection()"
   ```

**Benefits of SendGrid over Gmail SMTP**:

- **Higher deliverability** - Professional email service
- **Better analytics** - Track email delivery
- **No rate limits** - SendGrid handles scaling
- **Security** - API key instead of password
- **Production ready** - Built for applications

# Frontend Setup

cd ../frontend/Login-OTP
npm install

# Start Services

## Option 1: Use the automated script (Recommended)

cd ../../
./run_local_development.sh

## Option 2: Manual startup

### Terminal 1: Backend

cd backend
source venv/bin/activate
python -m uvicorn main:app --host 0.0.0.0 --port 8001 --reload

### Terminal 2: Frontend

cd ../frontend/Login-OTP
npm run dev

### Local Development: http://localhost:5173

### Deployed Frontend: https://backend-authentication-otp-6kyb.vercel.app/

### Deployed Backend: https://backend-authentication-otp.onrender.com/docs

### Deployed Application

### Live URLs

- **Frontend**: https://backend-authentication-otp-6kyb.vercel.app/
- **Backend API**: https://backend-authentication-otp.onrender.com/api
- **API Documentation**: https://backend-authentication-otp.onrender.com/docs

### Features

- SendGrid email integration with themed templates
- OTP authentication system
- User registration and login
- Phone number validation for 48+ countries
- Modern black/red theme design
- Real-time OTP delivery

### Option 3: CLI Interface

```bash
# Run CLI Application
python3 cli_app.py
```

## Data Models (CLI Style)

### User Model

```python
class User:
    id: int                    # Primary key
    username: str              # Unique, min 3 chars
    email: str                 # Unique, valid email
    phone_number: str          # Optional, with country code
    password: str              # Hashed with bcrypt
    created_at: datetime       # Registration timestamp

    # Relationships
    otp_codes: List[OTP]       # One-to-many
    login_attempts: List[LoginAttempt]  # One-to-many
```

### OTP Model

```python
class OTP:
    id: int                    # Primary key
    user_id: int               # Foreign key to User
    code: str                  # 6-digit secure random
    created_at: datetime       # Generation time
    expires_at: datetime       # 10 minutes expiry
    is_used: bool              # Single-use flag

    # Methods
    is_expired() -> bool       # Check expiry
    is_valid() -> bool         # Check if usable
```

### LoginAttempt Model

```python
class LoginAttempt:
    id: int                    # Primary key
    user_id: int               # Foreign key to User
    timestamp: datetime        # Attempt time
    successful: bool           # Success/failure
    ip_address: str            # Client IP (127.0.0.1)
```

## Legacy Domain Models

### User

1. Username must be unique and at least 3 characters long
2. Email must be unique and contain "@" symbol
3. Password must be at least 6 characters long
4. Password is hashed using bcrypt before storage
5. Has many OTP codes (one-to-many relationship)
6. Has many login attempts (one-to-many relationship)

### OTP (One-Time Password)

1. User must be a User instance (foreign key relationship)
2. Code is a 6-digit random number
3. Expires after 10 minutes from creation
4. Can only be used once (is_used flag)
5. Validates expiration before accepting

### LoginAttempt

1. User must be a User instance (foreign key relationship)
2. Tracks timestamp of each login attempt
3. Records success or failure status
4. Stores IP address (default: 127.0.0.1)
5. Enables login history tracking

## Error Handling

The application validates all inputs and provides clear error messages:

```python
# Username validation
user = User(username="ab")  # ValueError: Username too short

# Email validation
user = User(email="invalid-email")  # ValueError: Invalid email format

# Password validation
user.set_password("123")  # ValueError: Password must be at least 6 characters

# OTP validation
verify_otp(user_id, "999999")  # Returns: "Invalid OTP code"
verify_otp(user_id, expired_code)  # Returns: "OTP expired or already used"

# Profile update validation
update_user(username="existing_name")  # Returns: "Username already taken"
```

## Installation

### Quick Start (Single File Version)

1. **Install dependencies** (one-time setup):

```bash
pip install sqlalchemy bcrypt
```

2. **Save the code**:
   Copy the code from the artifact above and save as `auth_app.py`

3. **Run the application**:

```bash
python auth_app.py
```

### Alternative Setup (Modular Version with Pipenv)

```bash
# Install pipenv
pipenv install

# Create project directory
mkdir auth-system
cd auth-system

# Install dependencies
pipenv install sqlalchemy bcrypt alembic

# Create folder structure
mkdir models services
touch models/__init__.py services/__init__.py

# Run the application
pipenv run python cli.py
```

## Testing

### Manual Testing

The application is interactive and tests itself through the CLI interface:

1. **Test Registration**:

```bash
python auth_app.py
# Select option 1 (Register)
# Try various inputs:
# - Short username (should fail)
# - Invalid email (should fail)
# - Short password (should fail)
# - Mismatched passwords (should fail)
# - Valid credentials (should succeed)
```

2. **Test Login & OTP**:

```bash
# Select option 2 (Login)
# Enter registered email and password
# Check console for OTP code
# Enter correct OTP (should succeed)
# Try expired/wrong OTP (should fail)
```

3. **Test Dashboard Features**:

```bash
# After successful login:
# Test option 1 - View Profile
# Test option 2 - Update Profile (try duplicate username)
# Test option 3 - View Login History
# Test option 4 - Clear Login History
# Test option 5 - Delete Account (type DELETE to confirm)
```

### Automated Testing (Optional)

Create a `tests/` directory with test files:

```bash
mkdir tests
# Add test_models.py, test_auth.py, etc.
pytest
```

## Features Implemented

### Core Features

- User registration with validation
- Secure password hashing (bcrypt)
- Email and password authentication
- OTP generation and verification
- Two-factor authentication flow
- User dashboard with profile management
- Profile update (username, email, password)
- Login history tracking
- Account deletion with cascade

### Technical Features

- SQLAlchemy ORM with 3 related tables
- One-to-many relationships (User → OTP, User → LoginAttempt)
- Property decorators for password management
- Input validation with clear error messages
- Session management
- Database auto-initialization
- Clean CLI interface with menus and navigation

### Security Features

- Password hashing with bcrypt salt
- OTP expiration (10 minutes)
- One-time use OTP codes
- Failed login attempt tracking
- Secure credential validation

## Design Decisions

### Database Design

- **SQLite**: Chosen for simplicity - no server required, perfect for learning
- **ORM Pattern**: SQLAlchemy provides clean abstraction over SQL
- **Cascade Deletion**: When a user is deleted, all related OTP codes and login attempts are automatically removed
- **Relationships**: Explicit one-to-many relationships using foreign keys

### Security Design

- **Bcrypt Hashing**: Industry-standard password hashing with automatic salting
- **OTP Expiration**: Time-based expiration prevents replay attacks
- **Single Use OTPs**: is_used flag ensures codes can't be reused
- **Validation**: All inputs validated before database operations

### Code Organization

- **Single File Version**: All code in one file for easy deployment and learning
- **Service Layer**: AuthService separates business logic from database operations
- **CLI Separation**: Clean separation between interface and logic
- **Method Organization**: Grouped by functionality (auth, profile, history)

### User Experience

- **Clear Menus**: Numbered options with clear descriptions
- **Visual Feedback**: Emojis and formatting for better readability
- **Error Messages**: Descriptive messages for all validation failures
- **Confirmation Prompts**: Dangerous operations (delete) require explicit confirmation
- **Session Persistence**: User stays logged in until manual logout

## Database Schema

```
users
├── id (Primary Key)
├── username (Unique, Not Null)
├── email (Unique, Not Null)
├── password (Hashed, Not Null)
└── created_at (Timestamp)

otp_codes
├── id (Primary Key)
├── user_id (Foreign Key → users.id)
├── code (6 digits)
├── created_at (Timestamp)
├── expires_at (Timestamp)
└── is_used (Boolean)

login_attempts
├── id (Primary Key)
├── user_id (Foreign Key → users.id)
├── attempt_time (Timestamp)
├── success (Boolean)
└── ip_address (String)
```

## File Structure

### Single File Version

```
auth-system/
├── auth_app.py          # Complete application (all-in-one)
└── auth_system.db       # Auto-generated SQLite database
```

### Modular Version

```
auth-system/
├── models/
│   ├── __init__.py
│   ├── user.py          # User model with password hashing
│   ├── otp.py           # OTP model with validation
│   └── login_attempt.py # Login tracking model
├── services/
│   ├── __init__.py
│   ├── auth_service.py  # Authentication business logic
│   └── email_service.py # Email sending (simulated)
├── database.py          # Database configuration
├── cli.py               # CLI interface
├── Pipfile              # Dependencies
├── README.md            # Documentation
└── auth_system.db       # Auto-generated database
```

## Usage Examples

### Registration Flow

```
   AUTHENTICATION SYSTEM
1. Register
2. Login
3. Exit

Enter your choice: 1

   USER REGISTRATION
Enter username: john_doe
Enter email: john@example.com
Enter password: ******
Confirm password: ******

   Registration successful!
Welcome, john_doe! You can now login.
```

### Login Flow

```
   USER LOGIN
Enter email: john@example.com
Enter password: ******

==================================================
  EMAIL SENT TO: john@example.com
  YOUR OTP CODE: 123456
  Valid for 10 minutes
==================================================

Enter OTP code: 123456

 Login successful!
```

### Dashboard

```
  DASHBOARD - Welcome, john_doe!

1. View Profile
2. Update Profile
3. View Login History
4. Clear Login History
5. Delete Account
6. Logout

Enter your choice: 1

  YOUR PROFILE
Username: john_doe
Email: john@example.com
Password: **********************************************************
Account Created: 2024-12-05 10:30:45
```

## Common Issues & Solutions

**Issue**: ModuleNotFoundError for sqlalchemy or bcrypt  
**Solution**: Install dependencies: `pip install sqlalchemy bcrypt`

**Issue**: Database locked error  
**Solution**: Close any other instances of the app, or delete `auth_system.db` and restart

**Issue**: OTP not showing  
**Solution**: OTP is printed to console after entering email/password - scroll up to see it

**Issue**: Can't update profile  
**Solution**: Make sure new username/email isn't already taken by another user

## Email Configuration

The current version **simulates email** by printing to console. To enable real emails:

1. Uncomment the production code in `EmailService` class
2. Configure Gmail SMTP settings:
   - Enable 2-factor authentication on your Google account
   - Generate an App Password (Settings → Security → App Passwords)
   - Replace `your-email@gmail.com` and `your-app-password`
3. Install email library: `pip install secure-smtplib`

## Future Enhancements

Potential improvements for learning:

- [ ] Add email verification on registration
- [ ] Implement password reset functionality
- [ ] Add session timeout
- [ ] Rate limiting for failed login attempts
- [ ] Export login history to CSV
- [ ] Add user roles and permissions
- [ ] Implement remember me functionality
- [ ] Add profile picture support

## Contributing

This is an educational project. Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m 'Add new feature'`)
6. Push to your branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## License

This project is created for educational purposes as part of a Python programming assessment focusing on ORM relationships and CLI applications.

## Author

**PATRICKSON MUNGAI**

Created as part of Authentication System Project - demonstrating SQLAlchemy ORM, password security, and CLI interface design.

## Acknowledgments

- SQLAlchemy documentation for ORM patterns
- Bcrypt library for secure password hashing
- Python community for CLI best practices

---

**Note**: This is an educational project designed to teach object-relational mapping, database relationships, and secure authentication practices. The code is structured for clarity and learning, making it ideal for beginner to intermediate Python developers.

## Learning Outcomes

By studying this project, you'll learn:

- SQLAlchemy ORM and database relationships
- Secure password hashing with bcrypt
- Two-factor authentication implementation
- CLI application design patterns
- Input validation and error handling
- Session management
- Database schema design
- Clean code organization and separation of concerns
