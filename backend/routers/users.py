from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import models
import schemas
from database import get_db
from auth import get_current_user
import services.users_service as users_service

router = APIRouter(tags=['users'])

@router.post("/register", response_model=schemas.UzytkownikResponse)
def register_user(user:schemas.UzytkownikCreate, db:Session = Depends(get_db)):
    return users_service.register_user(user, db)

@router.post("/login")
def login_user(creds:schemas.UzytkownikCreate, db:Session = Depends(get_db)):
    return users_service.login_user(creds, db)

@router.put("/update_email")
def update_email( data:schemas.EmailChange, current_user:models.UzytkownikDB=Depends(get_current_user), db:Session = Depends(get_db)):
    return users_service.update_email(data, current_user, db)

@router.put("/update_password")
def update_password(data:schemas.PasswordChange, current_user:models.UzytkownikDB=Depends(get_current_user), db:Session=Depends(get_db)):
    return users_service.update_password(data, current_user, db)