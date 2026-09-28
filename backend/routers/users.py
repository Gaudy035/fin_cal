from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import User
import schemas.user as schemas
from database import get_db
from auth import get_current_user
import services.users as service

router = APIRouter(
    tags = ["users"],
    prefix = "/user"
)

@router.post("/register", response_model = schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.register_user(user, db)

@router.post("/login")
def login_user(creds: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.login_user(creds, db)

@router.put("/update_email")
def update_email(
    data: schemas.EmailChange, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return service.update_email(data, current_user, db)

@router.put("/update_password")
def update_password(
    data: schemas.PasswordChange, current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return service.update_password(data, current_user, db)