from passlib.context import CryptContext
from . import schemas, models
from .role import Role
from fastapi import Depends
from .database import get_db
from sqlalchemy.orm import Session
from .logs import logger
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        Role.ADMIN.name: Role.ADMIN.description,
        Role.GUEST.name: Role.GUEST.description,
        Role.USER.name: Role.USER.description
    }
)


def get_password_hash(password: str) -> str:
    '''
    Creates hash from passed password

    :param password: password
    :type password: str
    :returns: hashed password
    :rtype: str
    '''
    # logger.debug(f"password to create hash: {password}")
    return pwd_context.hash(password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    '''
    Verifies password

    :returns: True if password matched hash, otherwise False
    :rtype: bool
    '''
    return pwd_context.verify(raw_password, hashed_password)
