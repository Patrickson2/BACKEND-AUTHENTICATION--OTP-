# This file sets up the database connection for our authentication system
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database file location - SQLite creates a file on your computer
DATABASE_URL = "sqlite:///auth_system.db"

# Step 1: Create the database engine (this connects to the database file)
engine = create_engine(DATABASE_URL)

# Step 2: Create a session factory (this lets us talk to the database)
SessionLocal = sessionmaker(bind=engine)

# Step 3: Create a base class for all our database tables
Base = declarative_base()

def get_database():
    """Get a connection to the database so we can read/write data"""
    # Create a new database session
    database_session = SessionLocal()
    
    # Return the session so other functions can use it
    return database_session

def create_all_tables():
    """Create all the database tables (users, otp_codes, login_attempts)"""
    # This looks at all our models and creates the tables in the database file
    Base.metadata.create_all(bind=engine)
    
    # After this runs, you'll see a file called "auth_system.db" in your folder