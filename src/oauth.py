from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Security, Depends
from fastapi.security import SecurityScopes
from datetime import datetime, timedelta
from .settings import jwtsettings
from .schemas import TokenPayload
from .utils import oauth2_scheme
from .logs import logger
from .role import Role
from .exception import (TokenExpiredException, 
                        InvalidTokenException,
                        PermissionException)


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None) -> str:
    '''
    Creates jwt token
    :param data: data to be added to payload
    :type data: dict
    :param expires_delta:  #FIXME jak to działa
    :type expires_delta: timedelta | None
    :returns: access token
    :rtype: str
    '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=jwtsettings().access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        jwtsettings().secret_key,
        algorithm=jwtsettings().algorithm)
    return encoded_jwt


def verify_access_token(token: str) -> TokenPayload:
    '''
    Verify if access token is correct and returns payload of the token

    :param token: jwt token
    :type token: str
    :returns: payload
    :rtype: schemas.TokenPayload, pydantic base model
    '''
    try:
        payload = jwt.decode(
            token,
            jwtsettings().secret_key,
            algorithms=jwtsettings().algorithm)
        payload = TokenPayload(**payload)
        # TODO: what if it will be other exception?
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise InvalidTokenException
    return payload


def get_user(security_scopes: SecurityScopes,
             token: str = Depends(oauth2_scheme)) -> TokenPayload:
    '''
    Verify if token is valid and returns token payload

    :param security_scope: fastapi models, which contain scopes information
    :type security_scope: SecurityScopes
    :param token: jwt token
    :type token: str
    :returns: jwt token payload
    :rtype: TokenPayload, pydantic basic model
    '''
    token_payload = verify_access_token(token)
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    if token_payload.scope not in security_scopes.scopes:
        raise PermissionException(authenticate_value)
    return token_payload


def get_active_user(current_user: TokenPayload = Security(get_user, scopes=[Role.ADMIN.name])):
    ''' 
    Wraper to get_user function. Added to scope role admin by default
    :param current_user: 
    '''
    return current_user