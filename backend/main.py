from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
import models
import schemas
from database import engine, get_db, Base
from typing import List
from passwords import hash_password, verify_password
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer

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


# region JWT

SECRET_KEY = "JWT_SECRET_KEY"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = 600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINS)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Nieautoryzowany dostęp")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail='Token jest niewazny lub wygasl')
    
    user = db.query(models.UzytkownikDB).filter(models.UzytkownikDB.id_uzytkownika == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Uzytkownik nie istnieje")
    return user

# endregion JWT

@app.get("/")
def read_root():
    return {'message':'API IS WORKING'}

# region wydatki/wplaty

@app.get('/transakcje', response_model=List[schemas.TransakcjaResponse])
def get_transakcje(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session=Depends(get_db)):
    transakcje = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika).order_by(desc(models.TransakcjaDB.data)).all()
    return transakcje

@app.get("/wplywy", response_model=List[schemas.TransakcjaResponse])
def get_wplywy(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    wplywy = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wplyw', models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika).all()
    return wplywy

@app.get("/wydatki", response_model=List[schemas.TransakcjaResponse])
def get_wydatki(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    wydatki = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wydatek', models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika).all()
    return wydatki

@app.post("/add_payment", response_model=schemas.TransakcjaResponse)
def add_payment(payment:schemas.TransakcjaCreate, db:Session = Depends(get_db), current_user:models.UzytkownikDB = Depends(get_current_user)):
    payment_data = payment.model_dump()
    payment_data["id_uzytkownika"] = current_user.id_uzytkownika

    new_payment = models.TransakcjaDB(**payment_data)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@app.post("/add_recurring", response_model=schemas.PowtarzalnaResponse)
def add_recurring(payment:schemas.PowtarzalnaCreate, db:Session = Depends(get_db), current_user:models.UzytkownikDB = Depends(get_current_user)):
    payment_data = payment.model_dump()
    payment_data["id_uzytkownika"] = current_user.id_uzytkownika

    new_recurring = models.PowtarzalnaDB(**payment_data)
    db.add(new_recurring)
    db.commit()
    db.refresh(new_recurring)
    return new_recurring

@app.get("/get_recurring", response_model=List[schemas.PowtarzalnaResponse])
def get_recurring(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    powtarzalne = db.query(models.PowtarzalnaDB).filter(models.PowtarzalnaDB.id_uzytkownika==current_user.id_uzytkownika).order_by(asc(models.PowtarzalnaDB.nastepny_termin)).all()
    return powtarzalne

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
    
    access_token = create_access_token(data = {"sub":str(user.id_uzytkownika)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "zalogowano pomyslnie"
    }

# endregion uzytkownik

# region kategorie

@app.get("/kategorie", response_model=List[schemas.Kategoria])
def get_kategoria(db:Session = Depends(get_db)):
    kategorie = db.query(models.KategoriaDB).all()
    return kategorie

# endregion kategorie