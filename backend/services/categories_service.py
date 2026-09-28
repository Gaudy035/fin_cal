import models
from sqlalchemy.orm import Session

def get_categories(db:Session):
    categories = db.query(models.KategoriaDB).all()
    return categories