from fastapi import FastAPI

app = FastAPI()

pacients = [
    {
        "name": "Gaston Gaitan",
        "phone_number": "3487235569",
        "email": "gaston-gaitan@hotmail.com",
        "document_picture": "doc_gaston_gaitan_3487235569.jpg"
    },
    {
        "name": "Nicolas Capdepon",
        "phone_number": "3487235569",
        "email": "nicolas-capdepon@hotmail.com",
        "document_picture": "doc_nico_capde_3487235569.jpg"
    },
    {
        "name": "Gaston Gaitan",
        "phone_number": "3487235569",
        "email": "gaston-gaitan@hotmail.com",
        "document_picture": "doc_gaston_gaitan_3487235569.jpg"
    },
    {
        "name": "Vicente pertossi",
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