from sqlalchemy import Column, Integer, String
from database import Base

class Pacients(Base):
    __tablename__ = "pacients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    document_picture = Column(String)