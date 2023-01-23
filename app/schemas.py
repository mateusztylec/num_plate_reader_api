from pydantic import BaseModel, EmailStr


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
    brand: str | None
    model: str | None
    num_plate: str
    user_id: UserBase | None = None


class VehicleCreate(VehicleBase):
    id: int

    class Config:
        orm_mode = True


class VehicleResponse(VehicleBase):
    pass

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str