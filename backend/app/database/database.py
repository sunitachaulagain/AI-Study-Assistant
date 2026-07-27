from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg2://postgres:2472@localhost:5432/ai_study_assistant"

engine = create_engine(DATABASE_URL, echo=True)
print("Database module loaded")

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

