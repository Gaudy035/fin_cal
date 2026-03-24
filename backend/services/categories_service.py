import models
from sqlalchemy.orm import Session

def get_kategoria(db:Session):
    kategorie = db.query(models.KategoriaDB).all()
    return kategorie