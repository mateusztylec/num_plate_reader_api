from fastapi import FastAPI
from .routers import events, vehicles, users
from .exception import (TokenExpiredException, 
                        InvalidTokenException,
                        PermissionException,
                        token_expire_exception_handler,
                        invalid_token_handler,
                        invalid_permission_handler)


app = FastAPI()

app.include_router(vehicles.router)
app.include_router(users.router)
app.include_router(events.router)

app.add_exception_handler(TokenExpiredException, token_expire_exception_handler)
app.add_exception_handler(InvalidTokenException, invalid_token_handler)
app.add_exception_handler(PermissionException, invalid_permission_handler)

