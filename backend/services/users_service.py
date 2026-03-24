from fastapi import HTTPException
from sqlalchemy.orm import Session
import models
import schemas
from passwords import hash_password, verify_password
from auth import create_access_token


def register_user(user:schemas.UzytkownikCreate, db:Session):
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

def login_user(creds:schemas.UzytkownikCreate, db:Session):
    user = db.query(models.UzytkownikDB).filter(models.UzytkownikDB.email == creds.email).first()

    if not user or not verify_password(creds.haslo, user.haslo):
        raise HTTPException(status_code=403, detail="Nieprawidlowy email lub haslo")
    
    access_token = create_access_token(data = {"sub":str(user.id_uzytkownika)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "zalogowano pomyslnie"
    }

def update_email( data:schemas.EmailChange, current_user:models.UzytkownikDB, db:Session):
    if not verify_password(data.current_pass, current_user.haslo):
        raise HTTPException(status_code=400, detail="Niepoprawne haslo")
    
    email_exists = db.query(models.UzytkownikDB).filter(models.UzytkownikDB.email==data.new_email).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email jest juz zajety")
    
    current_user.email=data.new_email
    db.commit()
    return{"message":"email zmienono pomyslnie"}

def update_password(data:schemas.PasswordChange, current_user:models.UzytkownikDB, db:Session):
    if not verify_password(data.current_pass, current_user.haslo):
        raise HTTPException(status_code=400, detail="Nieprawidlowe haslo")
    
    current_user.haslo = hash_password(data.new_pass)
    db.commit()
    return {"message": "Zmiana hasla pomyslna"}