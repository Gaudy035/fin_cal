from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
import schemas.user as schemas
from security.passwords import hash_password, verify_password
from security.auth import create_access_token

def register_user(user: schemas.UserCreate, db: Session):
    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )
    if db_user:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f'User with email: {user.email} already exists')
    
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

def login_user(creds: schemas.UserLogin, db: Session):
    user = (
        db.query(User)
        .filter(User.email == creds.email)
        .first()
    )

    if not user or not verify_password(creds.password, user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect email or password")
    
    access_token = create_access_token(data = {"sub": str(user.user_id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": "Login successful"
    }

def update_email(data: schemas.EmailChange, current_user: User, db: Session):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect password")
    
    email_exists = (
        db.query(User)
        .filter(User.email == data.new_email)
        .first()
    )
    if email_exists:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email is already taken")
    
    current_user.email=data.new_email
    db.commit()
    return {"message": "Email changed successfully"}

def update_password(data: schemas.PasswordChange, current_user: User, db: Session):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect password")
    
    current_user.password = hash_password(data.new_password)
    db.commit()
    return {"message": "Password changed successfully"}

def delete_user(data: schemas.UserDelete, current_user: User, db: Session):
    if not verify_password(data.password, current_user.password):
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Incorrect password")

    db.delete(current_user)
    db.commit()
    return {"message": "User deleted successfully"}