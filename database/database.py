from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

password = "password"
database = "main"
host = "localhost"

DATABASE_URL = f"postgresql://master:{password}@{host}/{database}"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
