from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Pacient(BaseModel):
    id: int
    name: str
    phone_number: str
    email: EmailStr
    document_picture: str

pacients = [
    {
        "id": 1,
        "name": "Gaston Gaitan",
        "phone_number": "3487235569",
        "email": "gaston-gaitan@hotmail.com",
        "document_picture": "doc_gaston_gaitan_3487235569.jpg"
    },
    {
        "id": 2,
        "name": "Nicolas Capdepon",
        "phone_number": "3487235569",
        "email": "nicolas-capdepon@hotmail.com",
        "document_picture": "doc_nico_capde_3487235569.jpg"
    },
    {
        "id": 3,
        "name": "Vicente ismael",
        "phone_number": "34872355629",
        "email": "nicolas-capdepon@hotmail.com",
        "document_picture": "doc_nico_capde_3487235569.jpg"
    },
]

@app.get("/show_all_pacients")
async def show_all_pacients():
    return pacients

@app.get("/filter_pacients")
async def filter_pacients(key: str, value: str):
    filtered_pacients = [pacient for pacient in pacients if value.lower() in pacient.get(key, "").lower()]
    return filtered_pacients

@app.post("/create_pacient")
async def create_pacient(pacient: Pacient):
    pacients.append(pacient.model_dump())
    return {"message": "Pacient created successfully"}

@app.put("/update_pacient/{pacient_id}")
async def update_pacient(pacient_id: int, key: str, value: str):
    for pacient in pacients:
        if pacient["id"] == pacient_id:
            pacient[key] = value
            return {"message": "Pacient updated successfully"}
    return {"error": "Pacient not found"}

@app.delete("/delete_pacient/{pacient_id}")
async def delete_pacient(pacient_id: int):
    for pacient in pacients:
        if pacient["id"] == pacient_id:
            pacients.remove(pacient)
            return {"message": "Pacient deleted successfully"}
    return {"error": "Pacient not found"}