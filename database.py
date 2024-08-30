from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the database URL from the environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Debugging: Print the database URL to check if it's loaded correctly
print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

# Check if the environment variable is None
if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("SQLALCHEMY_DATABASE_URL is not set. Check your .env file.")

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Configure the session and base class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
