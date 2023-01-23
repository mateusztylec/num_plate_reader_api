from fastapi import APIRouter, HTTPException, status, Depends
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from ..logs import logger
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix="/vehicles", tags=["vehicles"])

@router.get("/plates/{num_plate}", response_model=schemas.VehicleResponse, status_code=status.HTTP_200_OK)
def get_vehicle_by_num_plate(num_plate: str, db: Session = Depends(get_db)):
    num_plate = num_plate.replace(" ", "")
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.num_plate == num_plate).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with number plate {num_plate} does not exist")
    return vehicle


@router.get("/", response_model=list[schemas.VehicleResponse], status_code=status.HTTP_200_OK)
def get_vehicles(db: Session = Depends(get_db), limit: int = 5, skip: int = 0):
    res_lst = db.query(models.Vehicle).limit(limit).offset(skip).all()
    return res_lst


@router.get("/{id}", response_model=schemas.VehicleResponse, status_code=status.HTTP_200_OK)
def get_vehicle_by_id(id: int, db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vehicle with id {id} does not exist")
    return vehicle


@router.post("/", response_model=schemas.VehicleCreate, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: schemas.VehicleBase, db: Session = Depends(get_db)):
    logger.debug(f"vehicle: {vehicle}")
    vehicle_db = models.Vehicle(**vehicle.dict())
    try:
        db.add(vehicle_db)
        db.commit()
        db.refresh(vehicle_db)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Vehicle with %(vehicle.num_plate)s already exist!")

    if not vehicle_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wrong vehicle info")
    return vehicle_db

