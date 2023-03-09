from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from .database import Base
from sqlalchemy.sql.expression import text


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


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey(Vehicle.id, ondelete="CASCADE"))
    date = Column(DateTime, nullable = True, server_default=text('now()'))
