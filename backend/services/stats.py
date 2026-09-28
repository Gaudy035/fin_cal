from sqlalchemy.orm import Session
from models.user import User
from models.category import Category
from models.transaction import Transaction
from sqlalchemy import func

def get_stats(current_user: User, db: Session):
    stats = (
        db.query(Category.category_name.label("nazwa_kat"), 
            func.sum(Transaction.amount).label('total'))
            .join(Transaction, Category.category_id == Transaction.category_id)
            .filter(Transaction.user_id == current_user.user_id, 
                Transaction.transaction_type=='wydatek')
            .group_by(Category.category_name)
            .all()
    )
    return [{"category": stat.nazwa_kat, "kwota": stat.total} for stat in stats]

def get_summary(current_user: User, db: Session):
    summary = (
        db.query(Transaction.transaction_type, 
            func.sum(Transaction.amount).label('kwota'))
            .filter(User.user_id == current_user.user_id).
            group_by(Transaction.transaction_type)
            .all()
    )
    return [{"type": s.typ, "kwota": s.kwota} for s in summary]