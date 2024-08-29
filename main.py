from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

import model
from database import engine
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Message(BaseModel):
    titulo: str
    conteudo: str

@app.get("/")
def read_root():
    return {"Hello":"TESTE2"}

@app.post("/criar", status_code=201)
def criar_valores(nova_mensagem: Message):
    print(nova_mensagem)
    return {"Mensagem": f"Título: {nova_mensagem.titulo} Conteúdo: {nova_mensagem.conteudo}"}

@app.get("/quadrado/{num}")
def quadrado(num: int):
    return num ** 2