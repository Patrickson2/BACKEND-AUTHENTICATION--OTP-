# Simple database setup using SQLite
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLite database file
DATABASE_URL = "sqlite:///auth_system.db"

# Set up database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_database():
    """Get a database connection"""
    return SessionLocal()

def create_all_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)