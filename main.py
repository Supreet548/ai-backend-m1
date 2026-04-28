from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def home():
    return{"message":"Welcome to my backend"}

class User(BaseModel):
    name : str
    email : str
    age : int

@app.post("/create-user")
def create_user(user:User):
    return{"message": "User created successfully", "data": user}