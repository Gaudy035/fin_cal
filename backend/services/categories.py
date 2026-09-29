from models import Category
from sqlalchemy.orm import Session

def get_categories(db: Session):
    categories = db.query(Category).all()
    return categories