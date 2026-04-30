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

    users_list=[]

    for row in rows:
        users_list.append({
            "id":row[0],
            "name":row[1],
            "email":row[2],
            "age":row[3],
            "city":row[4]
        })

    return{
        "success":True,
        "data":users_list,
        "message": "Users fetched successfully"
    }

@router.get("/users/{user_id}")
def get_user(user_id:int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT*FROM users WHERE id = %s",(user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return{"success": False, "message":"User not found"}

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



