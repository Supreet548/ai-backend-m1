from fastapi import APIRouter,HTTPException
from app.schemas.user_schema import UserSchema, LoginSchema
from app.utils.user_helper import UserHelper
from app.logger import logger
from fastapi import Header
from app.dependencies.auth_dependency import get_current_user
from app.auth import create_access_token, verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from app.utils.security import verify_password
from app.services.user_service import (
    create_user_service,
    fetch_all_users,
    fetch_user_by_id,
    fetch_user_by_email
)

from app.schemas.user_schema import UserListResponse,SingleUserResponse

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

@router.get("/users", response_model=UserListResponse)
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
            "city":row[4],
            "role": row[6] 
        })


    logger.info(f"Returned {len(users_list)} users")

    return{
        "success":True,
        "data":users_list,
        "message": "Users fetched successfully"
    }
    
    
#Get user by ID
@router.get("/users/{user_id}",response_model=SingleUserResponse)
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
            "city": row[4],
            "role": row[6] 
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

    stored_password = row[5]  

    if not verify_password(user.password, stored_password):
        raise HTTPException(401, "Invalid credentials")
    

    token = create_access_token({
    "user_id": row[0],
    "role": row[6]   
    
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


    
    




@router.get("/protected")
def protected_route(user = Depends(get_current_user)):

    return {
        "message": "Access granted",
        "user": user
    }



@router.get("/admin")
def admin_route(user = Depends(get_current_user)):

    if user.get("role") != "admin":
        raise HTTPException(403, "Access denied")

    return {"message": "Welcome Admin"}