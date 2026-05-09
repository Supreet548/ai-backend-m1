from fastapi import APIRouter,HTTPException,Depends
from app.schemas.user_schema import UserSchema, LoginSchema
from app.schemas.user_schema import UserListResponse,SingleUserResponse
from app.utils.user_helper import UserHelper
from app.logger import logger
from app.dependencies.auth_dependency import get_current_user
from app.auth.auth_handler import create_access_token,verify_token
from app.utils.security import verify_password

from app.services.user_service import (
    create_user_service,
    fetch_all_users,
    fetch_user_by_id,
    fetch_user_by_email
)



router = APIRouter()

@router.post(
    "/users",
    tags=["Users"],
    summary="Create a new user",
    description="Register a new user and store details in database"
)
async def create_user(user: UserSchema):
    try:
        logger.info(f"Creating user: {user.name}")

        await create_user_service(user)   

        helper = UserHelper(user.name)

        return {
            "success": True,
            "message": helper.welcome()
        }

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )
    

#Fetch all users

@router.get("/users", response_model=UserListResponse, tags=["Users"])
async def get_users():
    try:
        logger.info("Fetching all users (async)")

        users = await fetch_all_users()

        logger.info(f"Returned {len(users)} users")

        return {
            "success": True,
            "message": "Users fetched successfully",
            "data": users
        }

    except Exception as e:
        logger.error(f"Error in async GET /users: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Database connection failed"
        )

    except Exception as e:
        logger.error(f"Error in async GET /users: {str(e)}")

        raise HTTPException(500, "Database connection failed")
    
    
@router.get(
    "/users/{user_id}",
    response_model=SingleUserResponse,
    tags=["Users"],
    summary="Fetch user by ID",
    description="Retrieve a single user using user ID"
)
async def get_user(user_id: int):   
    try:
        logger.info(f"Fetching user with id: {user_id}")

        user = await fetch_user_by_id(user_id)   

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

@router.post(
    "/login",
    tags=["Auth"],
    summary="Login user",
    description="Authenticate user and generate JWT token"
)
async def login(user: LoginSchema):
    try:
        row = await fetch_user_by_email(user.email)

    except Exception:
        raise HTTPException(500, "Database connection failed")

    if not row:
        raise HTTPException(404, "User not found")

    if not verify_password(user.password, row["password"]):
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
@router.get(
    "/protected",
    tags=["Protected"],
    summary="Protected route",
    description="Accessible only with valid JWT token"
)
async def protected_route(user = Depends(get_current_user)):
    return {
        "message": "Access granted",
        "user": user
    }


# ADMIN
@router.get(
    "/admin",
    tags=["Admin"],
    summary="Admin route",
    description="Accessible only by admin users"
)
async def admin_route(user = Depends(get_current_user)):

    if user.get("role") != "admin":
        raise HTTPException(403, "Access denied")

    return {"message": "Welcome Admin"}


