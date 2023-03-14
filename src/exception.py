from fastapi import Request, APIRouter
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/users", tags=["users"])

class TokenExpiredException(Exception):
    pass


class InvalidTokenException(Exception):
    pass

class PermissionException(Exception):
    def __init__(self, authenticate_method: str) -> None:
        ''' Authenticate method is a string which will be send in response as header.
        "WWW-Authenticate": authenticate_method 
        '''
        self.authenticate_method = authenticate_method


def token_expire_exception_handler(request: Request, exc: TokenExpiredException) -> JSONResponse:
    return JSONResponse(status_code = 401, 
                        content = {"detail": "The token has expired!"},
                        headers = {"WWW-Authenticate": "Bearer"})

def invalid_token_handler(request: Request, exc: TokenExpiredException) -> JSONResponse:
    return JSONResponse(status_code = 401,
                        content={"detail": "Token is invalid!"},
                        headers={"WWW-Authenticate": "Bearer"})

def invalid_permission_handler(request: Request, exc: PermissionException) -> JSONResponse:
    return JSONResponse(status_code= 401,
                        content={"detail": "Not enough permission"},
                        headers={"WWW-Authenticate": exc.authenticate_method})
