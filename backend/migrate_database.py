#!/usr/bin/env python3
"""
Database migration script to add missing phone_number column
"""

import sqlite3
import os

def migrate_database():
    """Add phone_number column to users table if it doesn't exist"""
    
    db_path = "auth_system.db"
    
    if not os.path.exists(db_path):
        print("Database not found. Creating new database...")
        # Create new database by importing main
        import main
        print("New database created successfully!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if phone_number column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'phone_number' not in columns:
            print("Adding phone_number column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN phone_number VARCHAR(20)")
            conn.commit()
            print("phone_number column added successfully!")
        else:
            print("phone_number column already exists!")
        
        # Check table structure
        cursor.execute("PRAGMA table_info(users)")
        print("\nCurrent users table structure:")
        for column in cursor.fetchall():
            print(f"  {column[1]} ({column[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error migrating database: {e}")
        if conn:
            conn.close()

if __name__ == "__main__":
    migrate_database()
