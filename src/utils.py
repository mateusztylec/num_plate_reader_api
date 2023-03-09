from passlib.context import CryptContext
from . import schemas, models
from fastapi import Depends
from .database import get_db
from sqlalchemy.orm import Session
from .logs import logger

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    logger.debug(f"password to create hash: {password}")
    return pwd_context.hash(password)

def verify_password(raw_password: str, hashed_password: str):
    '''
    @return True if password matched hash
    '''
    return pwd_context.verify(raw_password, hashed_password)

