from sqlalchemy import Column, Integer, String
from ..database import Base


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False)
    role_name = Column(String, unique=True, nullable=False)
