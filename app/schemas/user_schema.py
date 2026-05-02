from pydantic import BaseModel,EmailStr,Field
from typing import Optional


class UserSchema(BaseModel):
    name : str = Field(..., min_length=3,max_length=30)
    email : EmailStr
    password: str 
    age : int= Field(...,gt=18,lt=100)
    city: str


class LoginSchema(BaseModel):
    email: str
    password: str