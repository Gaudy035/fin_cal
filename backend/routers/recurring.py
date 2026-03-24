from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from typing import List
import schemas
import models
import services.recurring_service as recurring_service

router = APIRouter(tags=['recurring'])

@router.post("/add_recurring", response_model=schemas.PowtarzalnaResponse)
def add_recurring(payment:schemas.PowtarzalnaCreate, db:Session = Depends(get_db), current_user:models.UzytkownikDB = Depends(get_current_user)):
    return recurring_service.add_recurring(payment, db, current_user)

@router.get("/get_recurring", response_model=List[schemas.PowtarzalnaResponse])
def get_recurring(current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    return recurring_service.get_recurring(current_user, db)

@router.put("/modify_recurring/{id_t_powtarzalnej}", response_model=schemas.PowtarzalnaResponse)
def modify_recurring(id_t_powtarzalnej:int, data:schemas.PowtarzalnaUpdate, current_user:models.UzytkownikDB = Depends(get_current_user), db:Session = Depends(get_db)):
    return recurring_service.modify_recurring(id_t_powtarzalnej, data, current_user)