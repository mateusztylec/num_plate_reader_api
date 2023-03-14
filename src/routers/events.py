from fastapi import APIRouter, Response, Security, status, Depends, HTTPException
from ..schemas import Event, VehicleBase
from ..database import get_db
from ..role import Role
from ..oauth import get_active_user
from sqlalchemy.orm import Session
from ..models import models


router = APIRouter(prefix="/events", tags=["events"])


@router.get("/", 
            response_model=list[Event], 
            status_code=status.HTTP_200_OK)
def get_events(db: Session = Depends(get_db), 
               limit: int = 5, 
               skip: int = 0,
               user=Security(
                    get_active_user,
                    scopes=[Role.USER.name])):
    events = db.query(models.Event).limit(limit).offset(skip).all()
    return events


@router.get("/{id}", 
            response_model=Event, 
            status_code=status.HTTP_200_OK)
def get_events(id: int, 
               db: Session = Depends(get_db),
               user=Security(
                    get_active_user,
                    scopes=[Role.USER.name])):
    events = db.query(models.Event).filter(models.Event.id == id).first()
    if not events:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"There is not event with id {id}")
    return events


@router.get("/vehicles/{id}",
            response_model=list[Event],
            status_code=status.HTTP_200_OK)
def get_events_by_vehicle_id(
        id: int,
        db: Session = Depends(get_db),
        user = Security(
            get_active_user,
            scopes=[Role.USER.name]),
        limit: int = 5,
        skip: int = 0):
    events = db.query(
        models.Event).filter(
        models.Event.vehicle_id == id).limit(limit).offset(skip).all()
    if not events:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Vehicle with id: {id} does not exist!")
    return events


@router.get("/vehicles/plates/{num_plate}",
            response_model=list[Event],
            status_code=status.HTTP_200_OK)
def get_events_by_vehicle_id(
        num_plate: str,
        db: Session = Depends(get_db),
        user=Security(
            get_active_user,
            scopes=[Role.USER.name]),
        limit: int = 5,
        skip: int = 0):
    num_plate = num_plate.replace(" ", "")
    events = db.query(
        models.Event).join(
        models.Vehicle).filter(
            models.Vehicle.num_plate == num_plate).limit(limit).offset(skip).all()
    if not events:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with num_plate: {num_plate} does not exist!")
    return events


@router.delete("/{id}", 
            #    response_model=Response, 
               status_code=status.HTTP_200_OK)
def delete_event_by_id(id: int, 
                       db: Session = Depends(get_db),
                       user=Security(
                            get_active_user,
                            scopes=[Role.USER.name])):
    event_delete = db.query(models.Event).filter(models.Event.id == id)
    if not event_delete.first():
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"Event with id {id} does not exist")
    event_delete = event_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
