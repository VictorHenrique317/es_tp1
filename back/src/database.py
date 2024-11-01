from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from src.models import *
import os

load_dotenv()
MYSQL_DATABASE_URL = os.getenv("MYSQL_DATABASE_URL")
if not MYSQL_DATABASE_URL:
    raise ValueError("Database URL is missing. Please set the MYSQL_DATABASE_URL environment variable.")

engine = create_engine(MYSQL_DATABASE_URL)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
