from fastapi import Depends, APIRouter, HTTPException, Path, status, Form, UploadFile, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
from models import Patient
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

UPLOAD_DIR = "media/patient_document_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class PatientRequest(BaseModel):
    name: str = Field(min_length=1)
    phone_number: str = Field(min_length=6)
    email: EmailStr 
    document_picture_source: str | None = None

@router.get("/show_all_patients", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    patients = db.query(Patient).all()
    return patients

# Mejorar el filtrado de patientes
@router.get("/filter_patients", status_code=status.HTTP_200_OK)
async def filter_patients(user: user_dependency, key: str, value: str, db: db_dependency):
    patients = db.query(Patient).filter(getattr(Patient, key) == value).all()
    if not patients:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patients

@router.post("/create_patient", status_code=status.HTTP_201_CREATED)
async def create_patient(
    user: user_dependency,
    background_tasks: BackgroundTasks,
    db: db_dependency,
    name: str = Form(...),
    phone_number: str = Form(...),
    email: EmailStr = Form(...),
    image: UploadFile = Form(...)
):
    
    # Validate if a patient with the same email already exists
    existing_patient = db.query(Patient).filter(Patient.email == email).first()
    if existing_patient:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Patient with this email already exists")

    # Validate that the image is of type JPG
    if image.content_type != "image/jpeg":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only JPG images are allowed")

    # Create a new patient with the provided data
    patient = PatientRequest(
        name=name,
        phone_number=phone_number,
        email=email,
        document_picture_source=None  # Will be updated after saving the image
    )
    new_patient = Patient(**patient.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    # Save the image on the server with the patient's id as the filename
    image_path = os.path.join(UPLOAD_DIR, f"{new_patient.id}.jpg")
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())

    # Update the patient's document picture source
    new_patient.document_picture_source = image_path
    db.commit()
    db.refresh(new_patient)

    background_tasks.add_task(send_confirmation_email, new_patient, db)

    # ADD SMS FUNCTIONALITY HERE

    return new_patient

# Falta agregar restriccion en caso de que se actualice a otro email que ya existe
@router.put("/update_patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_patient(
    user: user_dependency,
    key: str,
    value: str,
    db: db_dependency,
    patient_id: int = Path(gt=0)
):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if not hasattr(patient, key):
        raise HTTPException(status_code=400, detail="Invalid attribute")

    setattr(patient, key, value)
    db.commit()
    db.refresh(patient)

    return patient

@router.delete("/delete_patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(user: user_dependency, db: db_dependency, patient_id: int = Path(gt=0)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient id not found")

    db.delete(patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
