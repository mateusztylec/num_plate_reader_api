from pydantic import BaseModel

class VehicleBase(BaseModel):
    brand: int
    model: int
    num_plate: int

class VehicleCreate(VehicleBase):
    id: int

class Vehicle(VehicleBase):
    class Config:
        orm_mode = True
