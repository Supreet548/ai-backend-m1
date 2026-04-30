from fastapi import APIRouter
from .schemas import UserSchema
from .utils import UserHelper
import asyncio

router = APIRouter()

users = []
@router.get("/")
async def root():
    return {"message": "Async API Running"}

@router.get("/about")
async def about():
    return{
        "project": "AI Backend M1"
    }



@router.post("/users")
async def create_user(user:UserSchema):
    users.append(user.model_dump())

    helper = UserHelper(user.name)
    

    return{
        "success": True,
        "message": helper.welcome(),
        "role": helper.role(),
        "data": user
    }


@router.get("/users")
async def get_users():
    return users

@router.get("/slow")
async def slow_api():
    await asyncio.sleep(5)
    return {"message":"Finished after 5 seconds"}

@router.get("/wait2")
async def wait_api():
    await asyncio.sleep(2)
    return{"message":"Finished after 2 seconds"}


@router.get("/hello")
async def hello_api():
    return{"message":"Hello Async World"}