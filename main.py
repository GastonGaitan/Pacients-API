import os
from typing import Optional
from fastapi import FastAPI, Form, Path, UploadFile
from pydantic import BaseModel, EmailStr, Field
from starlette import status
from fastapi import HTTPException

app = FastAPI()

# Directorio donde se guardarán las imágenes
UPLOAD_DIR = "media/pacient_document_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class Pacient(BaseModel):
    id: Optional[int] = Field(description="Unique identifier for the pacient", default=None)
    name: str = Field(min_length=1)
    phone_number: str = Field(min_length=6)
    email: EmailStr 
    document_picture_source: Optional[str] = Field(
        description="Path to the document picture",
        default=None
    )

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

# @app.post("/create_pacient", status_code=status.HTTP_201_CREATED)
# async def create_pacient(pacient: Pacient):
#     for existing_pacient in pacients:
#         if existing_pacient.email == pacient.email:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pacient with this email already exists")
#     new_pacient = Pacient(id=len(pacients) + 1, name=pacient.name, phone_number=pacient.phone_number, email=pacient.email, document_picture=pacient.document_picture)
#     pacients.append(new_pacient)
#     return {"message": "Pacient created successfully"}

@app.post("/create_pacient", status_code=status.HTTP_201_CREATED)
async def create_pacient(name: str = Form(), phone_number: str = Form(), email: EmailStr = Form(), image: UploadFile = Form()):
    """
    Crea un nuevo paciente con los datos proporcionados y guarda la imagen en el servidor.
    """
    # Validar si ya existe un paciente con el mismo email
    for existing_pacient in pacients:
        if existing_pacient.email == email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pacient with this email already exists")

    # Validar que la imagen sea de tipo JPG
    if image.content_type != "image/jpeg":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only JPG images are allowed")

    # Crear un nuevo paciente con los datos proporcionados
    new_pacient_id = len(pacients) + 1
    new_pacient = Pacient(
        id=new_pacient_id,
        name=name,
        phone_number=phone_number,
        email=email,
        document_picture_source=None  # Se actualizará después de guardar la imagen
    )

    # Guardar la imagen en el servidor con el nombre del id del paciente
    image_path = os.path.join(UPLOAD_DIR, f"{new_pacient_id}.jpg")
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())

    # Actualizar la fuente de la imagen del paciente
    new_pacient.document_picture_source = image_path
    pacients.append(new_pacient)

    return {"message": "Pacient created successfully", "pacient": new_pacient}


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
