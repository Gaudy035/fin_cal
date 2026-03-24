from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc
import models
import schemas


def add_recurring(payment:schemas.PowtarzalnaCreate, db:Session, current_user:models.UzytkownikDB):
    payment_data = payment.model_dump()
    payment_data["id_uzytkownika"] = current_user.id_uzytkownika

    new_recurring = models.PowtarzalnaDB(**payment_data)
    db.add(new_recurring)
    db.commit()
    db.refresh(new_recurring)
    return new_recurring

def get_recurring(current_user:models.UzytkownikDB, db:Session):
    powtarzalne = db.query(models.PowtarzalnaDB).filter(models.PowtarzalnaDB.id_uzytkownika==current_user.id_uzytkownika).order_by(asc(models.PowtarzalnaDB.nastepny_termin)).all()
    return powtarzalne

def modify_recurring(id_t_powtarzalnej:int, data:schemas.PowtarzalnaUpdate, current_user:models.UzytkownikDB, db:Session):
    recurring = db.query(models.PowtarzalnaDB).filter(models.PowtarzalnaDB.id_t_powtarzalnej==id_t_powtarzalnej, models.PowtarzalnaDB.id_uzytkownika==current_user.id_uzytkownika).first()

    if not recurring:
        raise HTTPException(status_code=404, detail="Nie znaleziono transakcji")
    
    update_data = data.model_dump(exclude={'id_uzytkownika'})
    for key, val in update_data.items():
        setattr(recurring, key, val)

    try:
        db.commit()
        db.refresh(recurring)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Blad zapisu: {e}")

    return recurring
