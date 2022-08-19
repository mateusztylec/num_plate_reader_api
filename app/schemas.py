from pydantic import BaseModel

class VehicleBase(BaseModel):
    brand: str
    model: str
    num_plate: str

class VehicleCreate(VehicleBase):
    id: int
    class Config:
        orm_mode = True

class Vehicle(VehicleBase):
    pass
    class Config:
        orm_mode = True
