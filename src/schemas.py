from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from .utils import get_password_hash
from .role import Role

# FIXME: extermary verbose, must be better solution


class UserUpdateRequest(BaseModel):
    email: EmailStr = None
    name: str = None
    surname: str = None
    password: str = None


class UserUpdateAdminRequest(UserUpdateRequest):
    id: int = None
    scope: str = None


class UserUpdateResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    name: str
    surname: str

    @validator("email")
    def create_hash(cls, v):
        return v.lower()

    @validator("name")
    def name_lower_case(cls, v: str):
        return v.lower()

    @validator("surname")
    def surname_lower_case(cls, v: str):
        return v.lower()


class UserLogin(BaseModel):
    username: str
    password: str


class UserCreateRequest(UserBase):
    password: str

    @validator("password")
    def create_hash(cls, v):
        return get_password_hash(v)


class UserCreatedResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserBaseForAdmin(UserBase):  # TODO: show users with scope value
    pass

    class Config:
        orm_mode = True
    # scope: str

    # @validator("scope")
    # def upper_letters(cls, v):
    #     return v.upper()

    # @validator("scope")
    # def only_available_scope(cls, v):
    #     available_scopes = map(lambda val: val['name'], Role)
    #     if v not in available_scopes:
    #         raise ValueError(f"There isn't scope named {v}")


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
        return v  # return v is important coz w/o return field gets null value


class VehicleCreated(VehicleBase):
    id: int

    class Config:
        orm_mode = True


class VehicleResponse(VehicleBase):
    pass

    class Config:
        orm_mode = True


class VehicleUpdate(VehicleBase):
    """ Class for updating vehicle. It blocks the possibility of changing num_plate """
    num_plate = "temp"  # override value because is required by VehicleBase class. #FIXME: must be better solution.
    id = "temp"

    @validator("num_plate", "id")
    def prohibit_updating_num_plate(cls, v):
        if v:
            raise ValueError("Updating number plate or id is prohibit!")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int
    scope: str
    exp: int


class Event(BaseModel):
    id: int
    vehicle_id: int
    date: datetime

    class Config:
        orm_mode = True
