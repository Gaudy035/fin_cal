from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
# ----- Baza -----
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db, Base
from typing import List


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get("/")
def read_root():
    return {'message':'API IS WORKING'}

@app.get("/wplywy", response_model=List[schemas.TransakcjaResponse])
def get_wplywy(db:Session = Depends(get_db)):
    wplywy = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wplyw').all()
    return wplywy

@app.get("/wydatki", response_model=List[schemas.TransakcjaResponse])
def get_wydatki(db:Session = Depends(get_db)):
    wydatki = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wydatek')
    return wydatki