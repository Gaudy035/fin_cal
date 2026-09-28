from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas.category as schemas
from database import get_db
from typing import List
import services.categories as service

router = APIRouter(
    tags = ["categories"],
    prefix = "/categories"
)

@router.get("", response_model = List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return service.get_categories(db)