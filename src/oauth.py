from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from .settings import jwtsettings
from .utils import oauth2_scheme
from fastapi import Depends

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=jwtsettings().access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwtsettings().secret_key, algorithm=jwtsettings().algorithm)
    return encoded_jwt

def verify_access_token(token: str) -> dict:
    '''
    Verify if access token is correct and returns payload of the token
    @return payload: dict
    '''
    try:
        payload = jwt.decode(token, jwtsettings().secret_key, algorithms=jwtsettings().algorithm)
    except ExpiredSignatureError:
        raise Exception("The token has expired!")
    except JWTError:
        raise Exception("Wrong JWT token!")
    return payload

def get_user_id(token: str = Depends(oauth2_scheme)):
    token_payload = verify_access_token(token)
    return token_payload["user_id"]