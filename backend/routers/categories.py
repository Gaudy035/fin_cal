from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
from database import get_db
from typing import List
import services.categories_service as categories_service

router = APIRouter(tags=['categories'])

@router.get("/kategorie", response_model=List[schemas.Kategoria])
def get_kategoria(db:Session = Depends(get_db)):
    return categories_service.get_kategoria(db)