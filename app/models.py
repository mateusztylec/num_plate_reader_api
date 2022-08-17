from sqlalchemy import Column, Integer, String
from .database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, nullable=False)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    num_plate = Column(String, nullable=False)

