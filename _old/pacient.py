
from pydantic import BaseModel, EmailStr

class Pacient(BaseModel):
    id: int
    name: str
    phone_number: str
    email: EmailStr
    document_picture: str