from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from backend.app.models import Base

load_dotenv() #loaods .env to retrieve database URL

DATABASE_URL = os.getenv("DATABASE_URL") # retrieves the URL and stores it

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal() #creates a session

    try: 
        yield db #let endpoint use session
    finally: 
        db.close #closes session when not needed
