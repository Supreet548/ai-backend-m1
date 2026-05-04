from fastapi import APIRouter,HTTPException,Depends
from app.schemas.user_schema import UserSchema, LoginSchema
from app.schemas.user_schema import UserListResponse,SingleUserResponse
from app.utils.user_helper import UserHelper
from app.logger import logger
from app.dependencies.auth_dependency import get_current_user
from app.auth.auth_handler import create_access_token
from app.utils.security import verify_password

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
async def get_users():
    try:
        logger.info("Fetching all users (async)")

        users = await fetch_all_users()

        logger.info(f"Returned {len(users)} users")

        return {
            "success": True,
            "data": users
        }

    except Exception as e:
        logger.error(f"Error in async GET /users: {str(e)}")

        raise HTTPException(500, "Database connection failed")
    
    
#Get user by ID
@router.get("/users/{user_id}", response_model=SingleUserResponse)
def get_user(user_id: int):
    try:
        logger.info(f"Fetching user with id: {user_id}")

        user = fetch_user_by_id(user_id)   # ✅ already dict

    except Exception:
        logger.error("Database connection failed in GET /users")

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    logger.info(f"Returned user having UserID {user_id}")

    return {
        "success": True,
        "data": user
    }


@router.post("/login")
def login(user: LoginSchema):
    try:
        row = fetch_user_by_email(user.email)

    except Exception:
        raise HTTPException(500, "Database connection failed")

    if not row:
        raise HTTPException(404, "User not found")

    stored_password = row["password"]   # ✅ cleaner (after service fix)

    if not verify_password(user.password, stored_password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({
        "user_id": row["id"],
        "role": row["role"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }



# PROTECTED
@router.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": user
    }


# ADMIN
@router.get("/admin")
def admin_route(user=Depends(get_current_user)):

    if user.get("role") != "admin":
        raise HTTPException(403, "Access denied")

    return {"message": "Welcome Admin"}