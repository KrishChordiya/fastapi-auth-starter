from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserCreate(UserLogin):
    username:str

