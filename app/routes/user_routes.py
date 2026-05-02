from fastapi import APIRouter,HTTPException
from app.schemas.user_schema import UserSchema, LoginSchema
from app.utils.user_helper import UserHelper
from app.logger import logger
from fastapi import Header

from app.auth import create_access_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from app.services.user_service import (
    create_user_service,
    fetch_all_users,
    fetch_user_by_id,
    fetch_user_by_email
)

router = APIRouter()

@router.post("/users")
def create_user(user:UserSchema):
    try:

        logger.info(f"Creating user: {user.name}")

        create_user_service(user)

        helper = UserHelper(user.name)

        return {
            "success": True,
            "message": helper.welcome()
        }
    
    except Exception:

        logger.error("Database connection failed")

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )
    

#Fetch all users

@router.get("/users")
def get_users():
    try:
        logger.info("Fetching all users")

        rows = fetch_all_users()

    except Exception:
        logger.error("Database connection failed in GET /users")

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    users_list=[]

    for row in rows:
        users_list.append({
            "id":row[0],
            "name":row[1],
            "email":row[2],
            "age":row[3],
            "city":row[4]
        })


    logger.info(f"Returned {len(users_list)} users")

    return{
        "success":True,
        "data":users_list,
        "message": "Users fetched successfully"
    }
    
    
#Get user by ID
@router.get("/users/{user_id}")
def get_user(user_id:int):
    try:

        logger.info(f"Fetching user with id: {user_id}")

        row = fetch_user_by_id(user_id)

    except Exception:

        logger.error("Database connection failed in GET /users")
        
        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    if not row:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    logger.info(f"Returned user having UserID {user_id} ")

    return {
        "success": True,
        "data": {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[3],
            "city": row[4]
        }
    }



@router.post("/login")
def login(user: LoginSchema):
    try:
        row = fetch_user_by_email(user.email)

    except Exception:
        raise HTTPException(500, "Database connection failed")

    if not row:
        raise HTTPException(404, "User not found")

    token = create_access_token({"user_id": row[0]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
    


security = HTTPBearer()

@router.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    payload = verify_token(token)

    if not payload:
        raise HTTPException(401, "Invalid token")

    return {
        "message": "Access granted",
        "user": payload
    }