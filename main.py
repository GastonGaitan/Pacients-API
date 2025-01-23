from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel, EmailStr, Field
from pacient import Pacient
from starlette import status
from fastapi import HTTPException


app = FastAPI()

# Agregar campos email confirmado y numero de telefono confirmado
class Pacient(BaseModel):
    id: Optional[int] = Field(description="Unique identifier for the pacient", default=None)
    name: str = Field(min_length=1)
    phone_number: str = Field(min_length=6)
    email: EmailStr 
    document_picture: str = Field(description="Path to the document picture", min_length=4)

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

@app.get("/show_all_pacients", status_code=status.HTTP_200_OK)
async def show_all_pacients():
    return pacients

@app.get("/filter_pacients", status_code=status.HTTP_200_OK)
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

# Las restricciones de numero de telefono y email no deberian aplicarse si el mail no esta confirmado
@app.post("/create_pacient", status_code=status.HTTP_201_CREATED)
async def create_pacient(pacient: Pacient):
    for existing_pacient in pacients:
        if existing_pacient.email == pacient.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pacient with this email already exists")
    new_pacient = Pacient(id=len(pacients) + 1, name=pacient.name, phone_number=pacient.phone_number, email=pacient.email, document_picture=pacient.document_picture)
    pacients.append(new_pacient)
    return {"message": "Pacient created successfully"}

@app.put("/update_pacient/{pacient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pacient(key: str, value: str, pacient_id: int = Path(gt=0, lt=len(pacients) + 1)):
    for pacient in pacients:
        if pacient.id == pacient_id:
            if hasattr(pacient, key):
                setattr(pacient, key, value)
                return {"message": "Pacient updated successfully"}
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Attribute '{key}' not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacient not found")

@app.delete("/delete_pacient/{pacient_id}", status_code=status.HTTP_200_OK)
async def delete_pacient(pacient_id: int = Path(gt=0)):
    for pacient in pacients:
        if pacient.id == int(pacient_id):
            pacients.remove(pacient)
            return {"message": "Pacient deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacient id not found")
