from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from .users import User


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    num_plate = Column(String, nullable=False, unique=True)
