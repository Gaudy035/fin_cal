import models.category as model;
from sqlalchemy.orm import Session

def get_categories(db:Session):
    categories = db.query(model.Category).all()
    return categories