from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from pacient import Pacient

app = FastAPI()

class Pacient(BaseModel):
    id: Optional[int] = Field(description="Unique identifier for the pacient", default=None)
    name: str
    phone_number: str
    email: EmailStr
    document_picture: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "John Doe",
                "phone_number": "123-456-7890",
                "email": "john.doe@gmail.com",
                "document_picture": "document_pacient_id_1.jpg"
            }
        }
    }

pacients = [
    Pacient(id=1, name="John Doe", phone_number="123-456-7890", email="johndoe@example.com", document_picture="path/to/document1.jpg"),
    Pacient(id=2, name="Jane Smith", phone_number="987-654-3210", email="janesmith@example.com", document_picture="path/to/document2.jpg"),
    Pacient(id=3, name="Alice Johnson", phone_number="555-555-5555", email="alicejohnson@example.com", document_picture="path/to/document3.jpg")
]

@app.get("/show_all_pacients")
async def show_all_pacients():
    return pacients

@app.get("/filter_pacients")
async def filter_pacients(key: str, value: str):
    filtered_pacients = []
    for pacient in pacients:
        if hasattr(pacient, key):
            attribute_value = getattr(pacient, key)
            if key == "id":
                if attribute_value == int(value):
                    filtered_pacients.append(pacient)
            else:
                if value.lower() in str(attribute_value).lower():
                    filtered_pacients.append(pacient)
    return filtered_pacients

@app.post("/create_pacient")
async def create_pacient(pacient: Pacient):
    new_pacient = Pacient(id=len(pacients) + 1, name=pacient.name, phone_number=pacient.phone_number, email=pacient.email, document_picture=pacient.document_picture)
    pacients.append(new_pacient)
    return {"message": "Pacient created successfully"}

@app.put("/update_pacient/{pacient_id}")
async def update_pacient(pacient_id: int, key: str, value: str):
    for pacient in pacients:
        if hasattr(pacient, key):
            setattr(pacient, key, value)
            return {"message": "Pacient updated successfully"}
    return {"error": "Pacient not found"}

@app.delete("/delete_pacient/{pacient_id}")
async def delete_pacient(pacient_id: int):
    for pacient in pacients:
        if pacient.id == int(pacient_id):
            pacients.remove(pacient)
            return {"message": "Pacient deleted successfully"}
    return {"error": "Pacient not found"}
