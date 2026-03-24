from fastapi import APIRouter, Depends
import models
import schemas
from sqlalchemy.orm import Session
from sqlalchemy import desc
from auth import get_current_user
from database import get_db
from typing import List
import services.transactions_service as transactions_service

router = APIRouter(tags=['transactions'])


@router.get('/transakcje', response_model=List[schemas.TransakcjaResponse])
def get_transakcje(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session=Depends(get_db)):
    return transactions_service.get_transakcje(current_user, db)

@router.get("/wplywy", response_model=List[schemas.TransakcjaResponse])
def get_wplywy(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    return transactions_service.get_wplywy(current_user, db)

@router.get("/wydatki", response_model=List[schemas.TransakcjaResponse])
def get_wydatki(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    return transactions_service.get_wydatki(current_user, db)

@router.post("/add_payment", response_model=schemas.TransakcjaResponse)
def add_payment(payment:schemas.TransakcjaCreate, db:Session = Depends(get_db), current_user:models.UzytkownikDB = Depends(get_current_user)):
    return transactions_service.add_payment(payment, db, current_user)