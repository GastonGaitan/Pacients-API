from sqlalchemy import Column, Integer, String
from database import Base

class Pacient(Base):
    __tablename__ = "pacients"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    document_picture_source = Column(String)