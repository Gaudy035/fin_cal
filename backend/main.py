from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db, Base
from typing import List
from passwords import hash_password, verify_password

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
def read_root():
    return {'message':'API IS WORKING'}

# region wydatki/wplaty

@app.get("/wplywy", response_model=List[schemas.TransakcjaResponse])
def get_wplywy(user_id:int, db:Session = Depends(get_db)):
    wplywy = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wplyw', models.TransakcjaDB.id_uzytkownika==user_id).all()
    return wplywy

@app.get("/wydatki", response_model=List[schemas.TransakcjaResponse])
def get_wydatki(user_id:int, db:Session = Depends(get_db)):
    wydatki = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wydatek', models.TransakcjaDB.id_uzytkownika==user_id).all()
    return wydatki

@app.post("/add_payment", response_model=schemas.TransakcjaResponse)
def add_payment(payment:schemas.TransakcjaCreate, db:Session = Depends(get_db)):
    new_payment = models.TransakcjaDB(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


# endregion wydatki/wplaty

# region uzytkownik

@app.post("/register", response_model=schemas.UzytkownikResponse)
def register_user(user:schemas.UzytkownikCreate, db:Session = Depends(get_db)):
    db_user = db.query(models.UzytkownikDB).filter(models.UzytkownikDB.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail=f'Uzytkownik z adresem {user.email} juz istnieje')
    
    hashed_pwd = hash_password(user.haslo)

    new_user = models.UzytkownikDB(
        imie = user.imie,
        nazwisko = user.nazwisko,
        email = user.email,
        haslo = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login_user(creds:schemas.UzytkownikCreate, db:Session = Depends(get_db)):
    user = db.query(models.UzytkownikDB).filter(models.UzytkownikDB.email == creds.email).first()

    if not user or not verify_password(creds.haslo, user.haslo):
        raise HTTPException(status_code=403, detail="Nieprawidlowy email lub haslo")
    
    return {
        "message": "Zalogowano pomyslnie",
        "user_id": user.id_uzytkownika
    }

# endregion uzytkownik

# region kategorie

@app.get("/kategorie", response_model=List[schemas.Kategoria])
def get_kategoria(db:Session = Depends(get_db)):
    kategorie = db.query(models.KategoriaDB).all()
    return kategorie

# endregion kategorie