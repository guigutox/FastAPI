from fastapi import FastAPI, Depends
import classes
import model
from database import engine, get_db
from sqlalchemy.orm import Session
from typing import List

from webscraping import scrape, saveDB
model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

@app.get("/", status_code=200)
def read_root():
    return {"Hello": "World"}

@app.get("/quadrado/{num}")
def quadrado(num: int):
    return num ** 2

@app.post("/criar", status_code=201)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.post("/scrape", status_code=200)
def scrape_and_save(db: Session = Depends(get_db)):
    categorias = scrape()
    saveDB(categorias)
    return {"message": "Scrape and save complete"}

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=200)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens