from pydantic import BaseModel,EmailStr,Field
from typing import Optional


class UserSchema(BaseModel):
    name : str = Field(..., min_length=3,max_length=30)
    email : EmailStr
    age : int= Field(...,gt=18,lt=100)
    phone:Optional[str]=None
    city: str


class LoginSchema(BaseModel):
    email: EmailStr