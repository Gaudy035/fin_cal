from models import Transaction, User
import schemas.transaction as schemas
from sqlalchemy.orm import Session
from sqlalchemy import desc
from enums import TransactionType

def get_transactions(current_user: User, db: Session):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.user_id)
        .order_by(desc(Transaction.transaction_date))
        .all()
    )
    return transactions

def get_income(current_user: User, db: Session):
    income = (
        db.query(Transaction)
        .filter(Transaction.transaction_type == TransactionType.INCOME, 
            Transaction.user_id == current_user.user_id)
        .order_by(desc(Transaction.transaction_date))
        .all()
    )
    return income

def get_expenses(current_user: User, db: Session):
    expenses = (
        db.query(Transaction)
        .filter(Transaction.transaction_type == TransactionType.EXPENSE, 
            Transaction.user_id == current_user.user_id)
        .order_by(desc(Transaction.transaction_date))
        .all()
    )
    return expenses

def add_payment(payment: schemas.TransactionCreate, db: Session, current_user: User):
    payment_data = payment.model_dump()
    payment_data["user_id"] = current_user.user_id

    new_payment = Transaction(**payment_data)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment
