from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
from typing import List
import schemas.recurring as schemas
from models.user import User
import services.recurring as service

router = APIRouter(
    tags=["recurring"],
    prefix="/recurring"
)

@router.post("", response_model = schemas.RecurringResponse)
def add_recurring(
    payment: schemas.RecurringCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    return service.add_recurring(payment, db, current_user)

@router.get("", response_model = List[schemas.RecurringResponse])
def get_recurring(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_recurring(current_user, db)

@router.put("/{id_t_powtarzalnej}", response_model = schemas.RecurringResponse)
def modify_recurring(
    recurring_id: int, 
    data: schemas.RecurringUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return service.modify_recurring(recurring_id, data, current_user, db)