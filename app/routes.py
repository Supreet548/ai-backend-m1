from fastapi import APIRouter
from .schemas import UserSchema
from .utils import UserHelper
from .database import get_connection

router = APIRouter()

@router.post("/users")
def create_user(user:UserSchema):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "Insert INTO users (name, email, age, city) VALUES(%s, %s, %s, %s)",
        (user.name, user.email, user.age, user.city)
    )

    conn.commit()
    cur.close()
    conn.close()

    helper = UserHelper(user.name)

    return {
        "success": True,
        "message": helper.welcome()
    }

@router.get("/users")
def get_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows