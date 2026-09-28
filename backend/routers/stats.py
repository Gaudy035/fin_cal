from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from security.auth import get_current_user
from models.user import User
import services.stats as service

router = APIRouter(
    tags = ["stats"],
    prefix = "/stats"
)

@router.get("")
def get_stats(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return service.get_stats(current_user, db)

@router.get('/summary')
def get_summary(current_user: User = Depends(get_current_user), db: Session=Depends(get_db)):
    return service.get_summary(current_user, db)
