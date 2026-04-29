from fastapi import FastAPI,Query
from pydantic import BaseModel,EmailStr,Field
from typing import Optional

app = FastAPI()

users = [] #temporary memory database

class User(BaseModel):
    name : str = Field(..., min_length=3,max_length=30)
    email : EmailStr
    age : int= Field(...,gt=18,lt=100)
    phone:Optional[str]=None


@app.get("/")
def home():
    return {"message":"API Running"}

@app.post("/users")
def create_user(user:User):
    users.append(user.model_dump())
    return{
        "success": True,
        "message":"User created successfully",
        "data": user
    }

@app.get("/users")
def get_users(limit:int = Query(10,gt=0,le=100)):
    return users[:limit]


