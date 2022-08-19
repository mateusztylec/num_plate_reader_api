from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/vehicles/{id}", response_model=schemas.Vehicle, status_code=status.HTTP_200_OK)
def get_vehicles_by_id(id: int, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {id} does not exist")
    return vehicle

@app.get("/vehicles/{num_plate}", response_model=schemas.Vehicle, status_code=status.HTTP_200_OK)
def get_vehicle_by_num_plate(num_plate: str, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.num_plate == num_plate).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with number plate {num_plate} does not exist")
    return vehicle

@app.post("/vehicles/", response_model=schemas.VehicleCreate, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: schemas.Vehicle, db: Session = Depends(get_db)):
    vehicle_db = models.Vehicle(**vehicle.dict())
    db.add(vehicle_db)
    db.commit()
    db.refresh(vehicle_db)
    if not vehicle_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong vehicle info")
    return vehicle_db

