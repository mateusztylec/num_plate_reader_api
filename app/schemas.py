from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str


class UserCreate(UserBase):
    password: str


class UserCreateResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class VehicleBase(BaseModel):
    brand: str | None = None
    model: str | None = None
    num_plate: str 
    user_id: int | None = None

    @validator("num_plate")
    def cant_contain_spaces(cls, v):
        return v.replace(" ", "")

    @validator("num_plate", "brand", "model")
    def upper_letter(cls, v):
        if v is not None:
            return v.upper()

    @validator("num_plate")
    def cant_be_empty_string(cls, v):
        if v == "":
            raise ValueError("Numer plate field can't be empty!")
        return v   #return v is important coz w/o return field gets null value



class VehicleCreate(VehicleBase):
    id: int

    class Config:
        orm_mode = True


class VehicleResponse(VehicleBase):
    pass

    class Config:
        orm_mode = True

class VehicleUpdate(VehicleBase):
    """ Class for updating vehicle. It blocks the possibility of changing num_plate """
    num_plate = "temp" # override value because is required by VehicleBase class. #FIXME: must be better solution. 
    id = "temp"
    @validator("num_plate", "id")
    def prohibit_updating_num_plate(cls, v):
        if v:
            raise ValueError("Updating number plate or id is prohibit!")
        

class Token(BaseModel):
    access_token: str
    token_type: str


class Event(BaseModel):
    id: int
    vehicle_id: int
    date: datetime

    class Config:
        orm_mode = True