from fastapi import APIRouter, HTTPException, status, Depends, Security
from .. import schemas
from ..models import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..logs import logger
from sqlalchemy.exc import IntegrityError
from ..utils import oauth2_scheme
from ..oauth import get_active_user
from ..role import Role


router = APIRouter(prefix="/vehicles", tags=["vehicles"])



@router.get("/plates/{num_plate}",
            response_model=schemas.VehicleResponse,
            status_code=status.HTTP_200_OK)
def get_vehicle_by_num_plate(
        num_plate: str,
        user=Security(get_active_user, scopes=[Role.USER.name]),
        db: Session = Depends(get_db)):
    '''
    Retrieve vehicle info.
    '''
    num_plate = num_plate.replace(" ", "")  # FIXME user can see only vehicles added by him/her
    vehicle = db.query(models.Vehicle).filter(
        models.Vehicle.num_plate == num_plate).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with number plate {num_plate} does not exist")
    return vehicle


@router.get("/",
            response_model=list[schemas.VehicleResponse],
            status_code=status.HTTP_200_OK)
def get_vehicles(
        db: Session = Depends(get_db),
        user: int = Depends(get_active_user),
        limit: int = 5,
        skip: int = 0):
    res_lst = db.query(models.Vehicle).limit(limit).offset(skip).all()
    return res_lst


@router.get("/{id}", response_model=schemas.VehicleResponse,
            status_code=status.HTTP_200_OK)
def get_vehicle_by_id(
        id: int,
        user = Security(get_active_user, scopes=[Role.USER.name]),
        db: Session = Depends(get_db)):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == id).first()
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {id} does not exist")
    return vehicle


@router.post("/", response_model=schemas.VehicleCreate,
             status_code=status.HTTP_201_CREATED)
def create_vehicle(
        vehicle: schemas.VehicleBase,
        user = Security(get_active_user, scopes=[Role.USER.name]),
        db: Session = Depends(get_db)):
    vehicle_db = models.Vehicle(**vehicle.dict())
    try:
        db.add(vehicle_db)  # TODO: check if db.rollback() is needed
        db.commit()
        db.refresh(vehicle_db)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Vehicle with %(vehicle.num_plate)s already exist!")

    if not vehicle_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wrong vehicle info")
    return vehicle_db


@router.put("/{id}", response_model=schemas.VehicleCreate,
            status_code=status.HTTP_200_OK)
def update_vehicle_by_id(
        id: int,
        vehicle: schemas.VehicleUpdate,
        user = Security(get_active_user, scopes=[Role.USER.name]),
        db: Session = Depends(get_db)):
    vehicle_query = db.query(models.Vehicle).filter(models.Vehicle.id == id)
    if not vehicle_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with id {id} does not exist!")

    vehicle_query.update(
        vehicle.dict(exclude_unset=True),
        synchronize_session=False)
    db.commit()
    return vehicle_query.first()


@router.put("/plates/{num_plate}",
            response_model=schemas.VehicleCreate,
            status_code=status.HTTP_200_OK)
# TODO: proper validate num_plate entry
def update_vehicle_by_num_plate(
        num_plate: str,
        vehicle: schemas.VehicleUpdate,
        user = Security(get_active_user, scopes=[Role.USER.name]),
        db: Session = Depends(get_db)):
    num_plate = num_plate.replace(" ", "")
    vehicle_query = db.query(models.Vehicle).filter(models.Vehicle.num_plate == num_plate)
    if not vehicle_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with number plate {num_plate} does not exist!")
    vehicle_query.update(vehicle.dict(exclude_unset=True),synchronize_session=False)
    db.commit()
    return vehicle_query.first()
