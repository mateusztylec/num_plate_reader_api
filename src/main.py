from fastapi import FastAPI, Depends
from .routers import events, vehicles, users

app = FastAPI()

app.include_router(vehicles.router)
app.include_router(users.router)
app.include_router(events.router)