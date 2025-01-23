from app.core.database import Base
from sqlalchemy import Column, Integer, String

class Pacient(Base):
    __tablename__ = "pacients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    

