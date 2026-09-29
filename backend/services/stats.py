from sqlalchemy.orm import Session
from models import User, Category, Transaction
from sqlalchemy import func
from enums import TransactionType

def get_stats(current_user: User, db: Session):
    stats = (
        db.query(Category.category_name, 
            func.sum(Transaction.amount).label('total'))
            .join(Transaction, Category.category_id == Transaction.category_id)
            .filter(Transaction.user_id == current_user.user_id, 
                Transaction.transaction_type==TransactionType.EXPENSE)
            .group_by(Category.category_name)
            .all()
    )
    return [{"category": stat.category_name, "amount": stat.total} for stat in stats]

def get_summary(current_user: User, db: Session):
    summary = (
        db.query(Transaction.transaction_type, 
            func.sum(Transaction.amount).label('amount'))
            .filter(Transaction.user_id == current_user.user_id).
            group_by(Transaction.transaction_type)
            .all()
    )
    return [{"type": s.transaction_type, "amount": s.amount} for s in summary]