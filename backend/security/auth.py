from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
import models
from database import get_db
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINS = int(os.getenv("TOKEN_EXPIRE_MINS"))

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
