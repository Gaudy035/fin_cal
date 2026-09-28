from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc
from models.recurring import Recurring
from models.user import User
import schemas.recurring as schemas


def add_recurring(data: schemas.RecurringCreate, db: Session, current_user:User):
    payment_data = data.model_dump()
    payment_data["user_id"] = current_user.user_id

    new_recurring = Recurring(**payment_data)
    db.add(new_recurring)
    db.commit()
    db.refresh(new_recurring)
    return new_recurring

def get_recurring(current_user: User, db: Session):
    recurring = (
        db.query(Recurring)
        .filter(Recurring.user_id == current_user.user_id)
        .order_by(asc(Recurring.next_date))
        .all()
    )
    return recurring

def modify_recurring(
    recurring_id: int, 
    data: schemas.RecurringUpdate, 
    current_user: User, 
    db: Session
):
    recurring = (
        db.query(Recurring)
        .filter(Recurring.recurring_id == recurring_id, 
            Recurring.user_id == current_user.user_id)
        .first()
    )

    if not recurring:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    update_data = data.model_dump(exclude={'user_id'})
    for key, val in update_data.items():
        setattr(recurring, key, val)

    try:
        db.commit()
        db.refresh(recurring)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error")

    return recurring
