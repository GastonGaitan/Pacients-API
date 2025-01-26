from fastapi import FastAPI
import models
from database import engine, SessionLocal
from routers import auth, patients

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(patients.router)
