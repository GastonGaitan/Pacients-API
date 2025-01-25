from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    

class Pacient(Base):
    __tablename__ = "pacients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    document_picture_source = Column(String)
    email_verified = Column(Boolean, default=False)