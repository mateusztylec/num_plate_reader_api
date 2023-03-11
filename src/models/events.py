from sqlalchemy import Column, Integer, ForeignKey, DateTime
from ..database import Base
from .vehicles import Vehicle
from sqlalchemy.sql.expression import text

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey(Vehicle.id, ondelete="CASCADE"))
    date = Column(DateTime, nullable = True, server_default=text('now()'))
