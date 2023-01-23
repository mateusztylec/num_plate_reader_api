from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'))
    brand = Column(String, nullable=True)
    model = Column(String, nullable=True)
    num_plate = Column(String, nullable=False, unique=True)
