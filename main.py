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
]

@app.get("/show_pacients")
async def show_pacients():
    return pacients