# Command Line Interface - all the menus and user interactions
import re
from lib.database import get_database
from lib.auth import register_new_user, login_user, log_successful_login, update_user_info, delete_user_account, get_user_by_id
from lib.otp_service import create_new_otp, verify_otp_code, send_otp_email
from lib.models import LoginAttempt

def is_valid_email(email):
    """Check if email format is correct"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def show_main_menu():
    """Display the main menu options"""
    print("\n" + "="*40)
    print("AUTHENTICATION SYSTEM")
    print("="*40)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("-"*40)

def show_user_dashboard(username):
    """Display user dashboard after login"""
    print("\n" + "="*40)
    print(f" WELCOME {username.upper()}!")
    print("="*40)
    print("1. View Profile")
    print("2. Update Profile")
    print("3. View Login History")
    print("4. Clear Login History")
    print("5. Delete Account")
    print("6. Logout")
    print("-"*40)

def register_user():
    """Handle user registration process"""
    print("\n CREATE NEW ACCOUNT")
    print("-"*30)
    
    username = input("Enter username: ").strip()
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    
    if len(username) < 3:
        print(" Username too short")
        return
    
    if not is_valid_email(email):
        print(" Invalid email")
        return
    
    if len(password) < 6:
        print("Password too short")
        return
    
    db = get_database()
    user = register_new_user(db, username, email, password)
    db.close()
    
    if user:
        print(f" Account created! Welcome {user.username}!")
    else:
        print(" Username or email already exists")

def login_user_with_otp():
    """Handle user login with OTP verification"""
    print("\n LOGIN")
    print("-"*30)
    
    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()
    
    db = get_database()
    user = login_user(db, email, password)
    
    if not user:
        print(" Wrong email or password")
        return None, None
    
    print(" Credentials correct!")
    
    # Generate and send OTP
    otp_code = create_new_otp(db, user.id)
    send_otp_email(user.email, otp_code)
    
    # Ask for OTP
    print("\n📱 ENTER OTP CODE")
    attempts = 3
    while attempts > 0:
        entered_otp = input(f"Enter OTP ({attempts} attempts left): ").strip()
        
        if verify_otp_code(db, user.id, entered_otp):
            log_successful_login(db, user.id)
            print(" Login successful!")
            return user, db
        else:
            attempts -= 1
            if attempts > 0:
                print(" Wrong OTP. Try again.")
    
    print(" Too many wrong attempts")
    return None, None

def show_user_profile(user, db):
    """Display user's profile information"""
    print("\n YOUR PROFILE")
    print("-"*30)
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password: {'*' * 8}")
    print(f"Created: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

def update_user_profile(user, db):
    """Handle profile updates"""
    print("\n UPDATE PROFILE")
    print("-"*30)
    print("Leave blank to keep current value")
    
    new_username = input(f"New username ({user.username}): ").strip()
    new_email = input(f"New email ({user.email}): ").strip()
    new_password = input("New password: ").strip()
    
    update_user_info(
        db, user,
        new_username=new_username if new_username else None,
        new_email=new_email if new_email else None,
        new_password=new_password if new_password else None
    )
    print(" Profile updated!")

def show_login_history(user, db):
    """Display user's login history"""
    print("\n LOGIN HISTORY")
    print("-"*40)
    
    attempts = db.query(LoginAttempt).filter(
        LoginAttempt.user_id == user.id
    ).order_by(LoginAttempt.timestamp.desc()).limit(10).all()
    
    if not attempts:
        print("No login history")
        return
    
    for attempt in attempts:
        status = "SUCCESS" if attempt.successful else " FAILED"
        # time = attempt.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        print(f"{time} - {status}")

def clear_login_history(user, db):
    """Clear user's login history"""
    confirm = input("Clear history? (y/n): ").strip().lower()
    
    if confirm == 'y':
        db.query(LoginAttempt).filter(LoginAttempt.user_id == user.id).delete()
        db.commit()
        print(" History cleared!")

def delete_account(user, db):
    """Handle account deletion"""
    print("\n DELETE ACCOUNT")
    print("-"*30)
    
    confirm = input("Type 'DELETE' to confirm: ").strip()
    
    if confirm == 'DELETE':
        delete_user_account(db, user)
        print(" Account deleted!")
        return True
    else:
        print("Cancelled")
        return False

def user_dashboard(user, db):
    """Handle user dashboard after login"""
    while True:
        show_user_dashboard(user.username)
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            show_user_profile(user, db)
        elif choice == '2':
            update_user_profile(user, db)
        elif choice == '3':
            show_login_history(user, db)
        elif choice == '4':
            clear_login_history(user, db)
        elif choice == '5':
            if delete_account(user, db):
                break
        elif choice == '6':
            print(" Logged out!")
            break
        else:
            print(" Invalid choice")
        
        input("\nPress Enter...")
    
    db.close()

def start_cli():
    """Main CLI function"""
    while True:
        show_main_menu()
        choice = input("Choose option: ").strip()
        
        if choice == '1':
            register_user()
        elif choice == '2':
            user, db = login_user_with_otp()
            if user:
                user_dashboard(user, db)
        elif choice == '3':
            print(" Goodbye!")
            break
        else:
            print(" Invalid choice")
        
        input("\nPress Enter...")