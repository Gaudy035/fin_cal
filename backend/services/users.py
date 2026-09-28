from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user import User
import schemas.user as schemas
from passwords import hash_password, verify_password
from auth import create_access_token


def register_user(user: User, db: Session):
    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )
    if db_user:
        raise HTTPException(status_code=409, detail=f'User with email: {user.email} already exists')
    
    hashed_pwd = hash_password(user.password)

    new_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        password = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(creds: schemas.UserCreate, db: Session):
    user = (
        db.query(User)
        .filter(User.email == creds.email)
        .first()
    )

    if not user or not verify_password(creds.haslo, user.haslo):
        raise HTTPException(status_code = 401, detail = "Incorrect email or password")
    
    access_token = create_access_token(data = {"sub": str(user.user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful"
    }

def update_email(data: schemas.EmailChange, current_user: User, db: Session):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code = 401, detail = "Incorrect password")
    
    email_exists = (
        db.query(User)
        .filter(User == data.new_email)
        .first()
    )
    if email_exists:
        raise HTTPException(status_code=409, detail="Email is already taken")
    
    current_user.email=data.new_email
    db.commit()
    return{"message": "Email changed successfully"}

def update_password(data: schemas.PasswordChange, current_user: User, db: Session):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    current_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}