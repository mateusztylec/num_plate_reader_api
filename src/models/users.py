from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from .roles import Role


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role_id = Column(
        Integer,
        ForeignKey(
            Role.id,
            ondelete="CASCADE"),
        nullable=False)
    role = relationship("Role")
