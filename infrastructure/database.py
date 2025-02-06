import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

DB_URL = os.getenv("DB_URL", "sqlite:///./tracker.db")

connect_args = {}

engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use the new 2.0 style
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables automatically (Demo only; use migrations in production)
Base.metadata.create_all(bind=engine)
