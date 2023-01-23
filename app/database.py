from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import settings
from .logs import logger

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings().database_username}:{settings().database_password}@{settings().database_host}:{settings().database_port}/{settings().database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # tworzymy silnik xd

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # database session

Base = declarative_base()  # deklarujemy baze, z tego korzystamy przy tworzeniu tabel

def get_db():
    logger.info("Get db")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
