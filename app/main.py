from fastapi import FastAPI, Depends
from .routers import vehicles
from .routers import users

app = FastAPI()

app.include_router(vehicles.router)
app.include_router(users.router)
