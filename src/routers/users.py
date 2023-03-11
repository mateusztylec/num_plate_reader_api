from fastapi import APIRouter, Security, status, Depends, HTTPException
from .. import schemas
from ..models import models
from ..role import Role
from ..database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..utils import oauth2_scheme
from ..authenticate import authenticate_user
from ..logs import logger
from ..oauth import create_access_token, get_user

router = APIRouter(prefix="/users", tags=["users"])



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
    user = authenticate_user(schemas.UserLogin(username=form_data.username, password=form_data.password), db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password", headers={"WWW-Authenticate": "Bearer"})
    token = create_access_token({"user_id": user.id, "scope": "USER"}) #by default we add user scope
    return {"token_type": "Bearer", "access_token": token} 


@router.get("/manage/", response_model=list[schemas.UserCreateResponse], status_code=status.HTTP_200_OK)
def get_users(user = Security(get_user, scopes=Role.ADMIN["name"]), db: Session = Depends(get_db)):
    '''
    Admin can see all users
    '''
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no users!")
    return users


@router.put("/manage/", response_model=schemas.UserBaseForAdmin, status_code=status.HTTP_200_OK)
def update_user(user_to_update: schemas.UserUpdateByAdmin, user = Security(get_users, scopes=Role.ADMIN["name"]), db: Session = Depends(get_db)):
    '''
    Admin can update user by id. Id and Email can't be updated

    :returns: user info with updated information
    :rtype: schemas.UserBaseForAdmin, pydantic base model
    '''
    user_query = db.query(models.User).filter(models.User.email == user_to_update.email)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user_to_update.email} not found!")
    user_query.update(user_to_update.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return user_query.first()
