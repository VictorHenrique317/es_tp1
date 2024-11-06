from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Database URL is missing. Please set the DATABASE_URL environment variable.")

# Get the absolute path for the database file
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE_PATH = os.path.join(BASE_DIR, 'test.db')  # Adjust to your folder structure

# SQLite database URL
#SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_URL}"

print(os.path.abspath(__file__))

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()
from src.models import *
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
