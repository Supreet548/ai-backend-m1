from pydantic import BaseModel,EmailStr,Field
from typing import Optional, List


class UserSchema(BaseModel):
    name : str = Field(..., min_length=3,max_length=30)
    email : EmailStr
    password: str 
    age : int= Field(...,gt=18,lt=100)
    city: str
    role: str = "user"


class LoginSchema(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    city: str
    role: str


class UserListResponse(BaseModel):
    success: bool
    data: List[UserResponse]
    message: str


class SingleUserResponse(BaseModel):
    success: bool
    data: UserResponse