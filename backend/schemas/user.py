from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    first_name:str
    last_name:str
    email:str

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    user_id:int
    is_active:bool | None
    model_config = ConfigDict(from_attributes=True)

class EmailChange(BaseModel):
    current_password:str
    new_email:str

class PasswordChange(BaseModel):
    current_password:str
    new_password:str
