# Simple Authentication System

A basic CLI authentication system with OTP verification.

## Features

- Register with username, email, password
- Login with OTP verification
- View and update profile
- Login history tracking
- Account deletion

## How to Run

1. Install dependencies:
```bash
pipenv install
```

2. Run the program:
```bash
pipenv shell
python main.py
```

## Usage

1. Choose "1" to register
2. Choose "2" to login
3. Enter OTP code shown in console
4. Use dashboard to manage profile

## Files

- `main.py` - Start here
- `lib/cli.py` - All menus
- `lib/auth.py` - Login/register functions
- `lib/models.py` - Database tables
- `lib/otp_service.py` - OTP codes
- `lib/database.py` - Database setup

## Notes

- OTP codes shown in console (simulates email)
- Database file created automatically
- Passwords are hashed for security