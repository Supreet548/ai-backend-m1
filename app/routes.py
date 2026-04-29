from fastapi import APIRouter
from .schemas import UserSchema
from .utils import UserHelper

router = APIRouter()

users = []

@router.post("/users")
def create_user(user:UserSchema):
    users.append(user.model_dump())

    helper = UserHelper(user.name)
    

    return{
        "success": True,
        "message": helper.welcome(),
        "role": helper.role(),
        "data": user
    }


@router.get("/users")
def get_users():
    return users