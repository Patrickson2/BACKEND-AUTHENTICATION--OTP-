# This file handles all the menus and user interactions
from lib.database import get_database
from lib.auth import register_new_user, login_user, log_successful_login, update_user_info, delete_user_account, get_user_by_id
from lib.otp_service import create_new_otp, verify_otp_code, send_otp_email
from lib.models import LoginAttempt

def is_valid_email(email):
    """Check if email has correct format"""
    # Email must have @ symbol
    if "@" not in email:
        return False

    # Split email into name and domain parts
    name, _, domain = email.partition("@")

    # Domain must have a dot (like .com, .org)
    if "." not in domain:
        return False

    # Both name and domain must exist
    if not name or not domain:
        return False

    return True

def show_main_menu():
    """Show the main menu options"""
    print("\n" + "="*40)
    print(" AUTHENTICATION SYSTEM")
    print("="*40)
    print("1. Register (Create new account)")
    print("2. Login (Sign into account)")
    print("3. Exit (Close program)")
    print("-"*40)

def show_user_dashboard(username):
    """Show user menu after login"""
    print("\n" + "="*40)
    print(f" WELCOME {username.upper()}!")
    print("="*40)
    print("1. View Profile (See my details)")
    print("2. Update Profile (Change my details)")
    print("3. View Login History (See login attempts)")
    print("4. Clear Login History (Delete login records)")
    print("5. Delete Account (Remove my account)")
    print("6. Logout (Sign out)")
    print("-"*40)

# def register_user():
#     """Handle creating a new user account"""
#     print("\n CREATE NEW ACCOUNT")
#     print("-"*30)
    
#     # Get user input
#     username = input("Enter username: ").strip()
#     email = input("Enter email: ").strip()
#     password = input("Enter password: ").strip()
    
#     # Check if username is long enough
#     if len(username) < 3:
#         print(" Username too short (need at least 3 characters)")
#         return
    
#     # Check if email format is correct
#     if not is_valid_email(email):
#         print(" Invalid email format")
#         return
    
#     # Check if password is long enough
#     if len(password) < 6:
#         print(" Password too short (need at least 6 characters)")
#         return
    
#     # Connect to database
#     db = get_database()
    
#     # Try to create new user
#     user = register_new_user(db, username, email, password)
    
#     # Close database connection
#     db.close()
    
#     # Check if user was created successfully
#     if user:
#         print(f" Account created! Welcome {user.username}!")
#     else:
#         print(" Username or email already exists")

# def login_user_with_otp():
#     """Handle user login with OTP code verification"""
#     print("\n LOGIN")
#     print("-"*30)
    
#     # Get login details from user
#     email = input("Enter email: ").strip()
#     password = input("Enter password: ").strip()
    
#     # Connect to database
#     db = get_database()
    
#     # Check if email and password are correct
#     user = login_user(db, email, password)
    
#     # If login failed, stop here
#     if not user:
#         print(" Wrong email or password")
#         return None, None
    
#     print(" Email and password are correct!")
    
#     # Step 1: Create OTP code for this user
#     otp_code = create_new_otp(db, user.id)
    
#     # Step 2: Send OTP code to user's email (simulated)
#     send_otp_email(user.email, otp_code)
    
#     # Step 3: Ask user to enter the OTP code
#     print("\n📱 ENTER OTP CODE")
#     print("Check the email message above for your code")
    
#     # Give user 3 chances to enter correct OTP
#     attempts = 3
#     while attempts > 0:
#         entered_otp = input(f"Enter OTP code ({attempts} attempts left): ").strip()
        
#         # Check if OTP code is correct
#         if verify_otp_code(db, user.id, entered_otp):
#             # OTP is correct - record successful login
#             log_successful_login(db, user.id)
#             print(" Login successful!")
#             return user, db  # Return user and database connection
#         else:
#             # OTP is wrong - reduce attempts
#             attempts -= 1
#             if attempts > 0:
#                 print(" Wrong OTP code. Try again.")
    
#     # Too many wrong attempts
#     print(" Too many wrong attempts")
#     return None, None

# def show_user_profile(user, db):
#     """Display user's profile information"""
#     print("\n YOUR PROFILE")
#     print("-"*30)
#     print(f"Username: {user.username}")
#     print(f"Email: {user.email}")
#     print(f"Password: {'*' * 8} (hidden for security)")
#     print(f"Account created: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

# def update_user_profile(user, db):
#     """Let user change their profile details"""
#     print("\n UPDATE PROFILE")
#     print("-"*30)
#     print("Leave blank to keep current value")
    
#     # Get new values (user can leave blank to keep current)
#     new_username = input(f"New username (current: {user.username}): ").strip()
#     new_email = input(f"New email (current: {user.email}): ").strip()
#     new_password = input("New password: ").strip()
    
#     # Update the user's information
#     update_user_info(
#         db, user,
#         new_username=new_username if new_username else None,
#         new_email=new_email if new_email else None,
#         new_password=new_password if new_password else None
#     )
#     print(" Profile updated!")

# def show_login_history(user, db):
#     """Show user's past login attempts"""
#     print("\n LOGIN HISTORY")
#     print("-"*40)
    
#     # Get last 10 login attempts from database
#     attempts = db.query(LoginAttempt).filter(
#         LoginAttempt.user_id == user.id
#     ).order_by(LoginAttempt.timestamp.desc()).limit(10).all()
    
#     # Check if user has any login history
#     if not attempts:
#         print("No login history found")
#         return
    
#     # Show each login attempt
#     for attempt in attempts:
#         # Show if login was successful or failed
#         if attempt.successful:
#             status = " SUCCESS"
#         else:
#             status = " FAILED"
        
#         # Format the time nicely
#         time = attempt.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#         print(f"{time} - {status}")

# def clear_login_history(user, db):
#     """Delete all login history for this user"""
#     # Ask user to confirm
#     confirm = input("Clear all login history? (y/n): ").strip().lower()
    
#     # Only delete if user types 'y'
#     if confirm == 'y':
#         # Delete all login attempts for this user
#         db.query(LoginAttempt).filter(LoginAttempt.user_id == user.id).delete()
#         # Save changes to database
#         db.commit()
#         print(" Login history cleared!")

# def delete_account(user, db):
#     """Delete user's account completely"""
#     print("\n DELETE ACCOUNT")
#     print("-"*30)
#     print("WARNING: This will delete your account forever!")
    
#     # Ask user to type 'DELETE' to confirm
#     confirm = input("Type 'DELETE' to confirm: ").strip()
    
#     # Only delete if user types exactly 'DELETE'
#     if confirm == 'DELETE':
#         # Delete the user account
#         delete_user_account(db, user)
#         print(" Account deleted!")
#         return True  # Account was deleted
#     else:
#         print("Account deletion cancelled")
#         return False  # Account was not deleted

# def user_dashboard(user, db):
#     """Main menu after user logs in"""
#     # Keep showing menu until user logs out
#     while True:
#         # Show the dashboard menu
#         show_user_dashboard(user.username)
        
#         # Get user's choice
#         choice = input("Choose an option (1-6): ").strip()
        
#         # Handle each menu option
#         if choice == '1':
#             # Show user's profile
#             show_user_profile(user, db)
#         elif choice == '2':
#             # Update user's profile
#             update_user_profile(user, db)
#         elif choice == '3':
#             # Show login history
#             show_login_history(user, db)
#         elif choice == '4':
#             # Clear login history
#             clear_login_history(user, db)
#         elif choice == '5':
#             # Delete account
#             if delete_account(user, db):
#                 break  # Exit dashboard if account deleted
#         elif choice == '6':
#             # Logout
#             print(" Logged out successfully!")
#             break  # Exit dashboard
#         else:
#             # Invalid choice
#             print(" Invalid choice. Please enter 1-6.")
        
#         # Wait for user to press Enter before showing menu again
#         input("\nPress Enter to continue...")
    
#     # Close database connection when done
#     db.close()

# def start_cli():
#     """Main function that runs the program"""
#     # Keep showing main menu until user exits
#     while True:
#         # Show the main menu
#         show_main_menu()
        
#         # Get user's choice
#         choice = input("Choose an option (1-3): ").strip()
        
#         # Handle each menu option
#         if choice == '1':
#             # Register new user
#             register_user()
#         elif choice == '2':
#             # Login existing user
#             user, db = login_user_with_otp()
#             # If login successful, show user dashboard
#             if user:
#                 user_dashboard(user, db)
#         elif choice == '3':
#             # Exit program
#             print(" Goodbye!")
#             break  # Exit the program
#         else:
#             # Invalid choice
#             print(" Invalid choice. Please enter 1-3.")
        
#         # Wait for user to press Enter before showing menu again
#         input("\nPress Enter to continue...")