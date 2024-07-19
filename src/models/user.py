from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    is_active = Column(Boolean)
    is_supervisor = Column(Boolean)

