#!/usr/bin/env python3
"""
Main file - Start the program here
"""
from lib.database import create_all_tables
from lib.cli import start_cli

def main():
    """Start the authentication system"""
    print(" Starting Authentication System...")
    
    # Create database tables
    create_all_tables()
    print("Database ready")
    
    # Start the program
    start_cli()

if __name__ == "__main__":
    main()