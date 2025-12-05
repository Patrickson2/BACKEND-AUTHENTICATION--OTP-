#!/usr/bin/env python3
"""
This is the main file - the starting point of our authentication system program
When you run "python main.py", this is the file that gets executed first
"""

# Import the functions we need from other files
from lib.database import create_all_tables
from lib.cli import start_cli

def main():
    """This is the main function that starts our entire authentication system"""
    
    # Step 1: Welcome message to let user know the program is starting
    print(" Starting Authentication System...")
    print("Setting up the system for you...")
    
    # Step 2: Create the database tables if they don't exist yet
    # This creates the users, otp_codes, and login_attempts tables
    create_all_tables()
    print(" Database is ready!")
    
    # Step 3: Start the command line interface (the menus and user interaction)
    # This is where users can register, login, and manage their accounts
    print("Starting the main program...")
    start_cli()
    
    # Step 4: Program has ended
    print("Authentication system has been closed. Goodbye!")

# This special code block runs when you execute this file directly
# It means: "If someone runs 'python main.py', then call the main() function"
if __name__ == "__main__":
    main()