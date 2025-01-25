from fastapi import Depends, APIRouter, HTTPException, Path, status, Form, UploadFile, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
from models import Pacient
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
import os
from .auth import get_current_user
import smtplib
from email.mime.multipart import MIMEMultipart
from helpers.send_confirmation_email import send_confirmation_email
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

UPLOAD_DIR = "media/pacient_document_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class PacientRequest(BaseModel):
    name: str = Field(min_length=1)
    phone_number: str = Field(min_length=6)
    email: EmailStr 
    document_picture_source: str | None = None

@router.get("/show_all_pacients", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    pacients = db.query(Pacient).all()
    return pacients

# Mejorar el filtrado de pacientes
@router.get("/filter_pacients", status_code=status.HTTP_200_OK)
async def filter_pacients(user: user_dependency, key: str, value: str, db: db_dependency):
    pacients = db.query(Pacient).filter(getattr(Pacient, key) == value).all()
    if not pacients:
        raise HTTPException(status_code=404, detail="Pacient not found")
    return pacients

@router.post("/create_pacient", status_code=status.HTTP_201_CREATED)
async def create_pacient(
    user: user_dependency,
    background_tasks: BackgroundTasks,
    db: db_dependency,
    name: str = Form(...),
    phone_number: str = Form(...),
    email: EmailStr = Form(...),
    image: UploadFile = Form(...)
):
    
    # Validate if a pacient with the same email already exists
    existing_pacient = db.query(Pacient).filter(Pacient.email == email).first()
    if existing_pacient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pacient with this email already exists")

    # Validate that the image is of type JPG
    if image.content_type != "image/jpeg":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only JPG images are allowed")

    # Create a new pacient with the provided data
    pacient = PacientRequest(
        name=name,
        phone_number=phone_number,
        email=email,
        document_picture_source=None  # Will be updated after saving the image
    )
    new_pacient = Pacient(**pacient.model_dump())
    db.add(new_pacient)
    db.commit()
    db.refresh(new_pacient)

    # Save the image on the server with the pacient's id as the filename
    image_path = os.path.join(UPLOAD_DIR, f"{new_pacient.id}.jpg")
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())

    # Update the pacient's document picture source
    new_pacient.document_picture_source = image_path
    db.commit()
    db.refresh(new_pacient)

    background_tasks.add_task(send_confirmation_email, email, name)

    return new_pacient

# Falta agregar restriccion en caso de que se actualice a otro email que ya existe
@router.put("/update_pacient/{pacient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_pacient(
    user: user_dependency,
    key: str,
    value: str,
    db: db_dependency,
    pacient_id: int = Path(gt=0)
):
    pacient = db.query(Pacient).filter(Pacient.id == pacient_id).first()
    if not pacient:
        raise HTTPException(status_code=404, detail="Pacient not found")

    if not hasattr(pacient, key):
        raise HTTPException(status_code=400, detail="Invalid attribute")

    setattr(pacient, key, value)
    db.commit()
    db.refresh(pacient)

    return pacient

@router.delete("/delete_pacient/{pacient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pacient(user: user_dependency, db: db_dependency, pacient_id: int = Path(gt=0)):
    pacient = db.query(Pacient).filter(Pacient.id == pacient_id).first()
    if not pacient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacient id not found")

    db.delete(pacient)
    db.commit()
    return {"message": "Pacient deleted successfully"}
