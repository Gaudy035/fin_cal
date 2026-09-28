from fastapi import APIRouter, Depends
from models.user import User
import schemas.transaction as schemas
from sqlalchemy.orm import Session
from security.auth import get_current_user
from database import get_db
from typing import List
import services.transactions as service

router = APIRouter(
    tags=["transactions"],
    prefix="/transactions"
)


@router.get("", response_model = List[schemas.TransactionResponse])
def get_transactions(current_user: User = Depends(get_current_user), db: Session=Depends(get_db)):
    return service.get_transactions(current_user, db)

@router.get("/income", response_model = List[schemas.TransactionResponse])
def get_income(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_income(current_user, db)

@router.get("/expenses", response_model = List[schemas.TransactionResponse])
def get_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_expenses(current_user, db)

@router.post("", response_model = schemas.TransactionResponse)
def add_payment(
        payment: schemas.TransactionCreate, 
        db: Session = Depends(get_db), 
        current_user:User = Depends(get_current_user)
    ):
    return service.add_payment(payment, db, current_user)