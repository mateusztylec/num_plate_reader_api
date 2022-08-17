from fastapi import FastAPI
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/vehicles/{id}", response_model=schemas.Vehicle)
def get_vehicles_by_id(id: int, db: Session):
    return db.query(models.Vehicle).filter(models.Vehicle.id == id).first()

@app.post("/vehicles/", response_model=schemas.VehicleCreate)
def create_vehicle()

