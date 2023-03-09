from fastapi import APIRouter, status, Depends, HTTPException
from .. import models, schemas
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..utils import verify_password, get_password_hash
from ..authenticate import authenticate_user
from ..logs import logger

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[schemas.UserCreateResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no users!")
    return users


@router.post("/", response_model=schemas.UserCreateResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_to_create: schemas.UserCreate, db: Session = Depends(get_db)):
    # user_lowercase = schemas.UserBase(**{_: v.lower() for _, v in user_to_create.dict().items()})  #TODO: jak to działa bez klucza
    # new_user = schemas.UserCreate(password=user_to_create.password, **user_lowercase.dict())
    user = models.User(**user_to_create.dict())
    db.add(user)
    try:
        db.commit()
    except IntegrityError: #TODO: co gdy będzie inny wyjątek
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user.email} already exists")
    db.refresh(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Can not create user!")
    return user

@router.post("/login/", response_model=schemas.Token, status_code=status.HTTP_202_ACCEPTED)
def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.debug(f"usr: {form_data.username}, pwd: {form_data.password}")
    user = schemas.UserLogin(username=form_data.username, password=form_data.password)
    if not authenticate_user(user, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorect username or password")
    return {"token_type": "token123", "access_token": "123"}

