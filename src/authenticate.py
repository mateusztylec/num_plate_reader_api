from . import schemas, models
from .utils import verify_password
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .logs import logger
from .oauth import create_access_token

def authenticate_user(user: schemas.UserLogin, db: Session) -> str | None:
    '''
    Check if user in db and if password if correct. If not return False in both cases.
    @param1 user: schemas.UserLogin
    @param2 db: Session
    @retrun user: sqlalchemy model or Flase
    '''
    user_db = db.query(models.User).filter(models.User.email == user.username).first()
    logger.debug(f"user_db: {user_db.password}")
    if not user_db:
        return False
    if not verify_password(user.password, user_db.password):
        logger.debug("password verification failed")
        return False
    # user = schemas.UserBase(**user_db.dict()) #TODO conversion sqlalchemy to pydantic
    return user_db