from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user
import models
import services.stats_service as stats_service

router = APIRouter(tags=['stats'])

@router.get('/get_stats')
def get_stats(current_user:models.UzytkownikDB=Depends(get_current_user), db:Session = Depends(get_db)):
    return stats_service.get_stats(current_user, db)

@router.get('/get_summary')
def get_summary(current_user:models.UzytkownikDB=Depends(get_current_user),db:Session=Depends(get_db)):
    return stats_service.get_summary(current_user, db)
