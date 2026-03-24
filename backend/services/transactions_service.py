import models
import schemas
from sqlalchemy.orm import Session
from sqlalchemy import desc

def get_transakcje(current_user:models.UzytkownikDB, db:Session):
    transakcje = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika).order_by(desc(models.TransakcjaDB.data)).all()
    return transakcje

def get_wplywy(current_user:models.UzytkownikDB, db:Session):
    wplywy = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wplyw', models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika).order_by(desc(models.TransakcjaDB.data)).all()
    return wplywy

def get_wydatki(current_user:models.UzytkownikDB, db:Session):
    wydatki = db.query(models.TransakcjaDB).filter(models.TransakcjaDB.typ == 'wydatek', models.TransakcjaDB.id_uzytkownika==current_user.id_uzytkownika).order_by(desc(models.TransakcjaDB.data)).all()
    return wydatki

def add_payment(payment:schemas.TransakcjaCreate, db:Session, current_user:models.UzytkownikDB):
    payment_data = payment.model_dump()
    payment_data["id_uzytkownika"] = current_user.id_uzytkownika

    new_payment = models.TransakcjaDB(**payment_data)
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment
