from app.database.connection import get_connection
from app.utils.security import hash_password
from app.database.async_connection import get_pool

#  Create User
async def create_user_service(user):
    pool = await get_pool()

    hashed_pwd = hash_password(user.password)  

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (name, email, age, city, password, role)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            user.name,
            user.email,
            user.age,
            user.city,
            hashed_pwd,  
            user.role
        )


#  Fetch All Users
async def fetch_all_users():
    pool = await get_pool()

    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM users")

        users = []

        for row in rows:
            users.append({
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "age": row["age"],
                "city": row["city"],
                "role": row["role"]
            })

        return users

   


#  Fetch User by ID
async def fetch_user_by_id(user_id):
    pool = await get_pool()

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            user_id
        )

    if not row:
        return None

    return {
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "age": row["age"],
        "city": row["city"],
        "role": row["role"]
    } 





#Fetch user by email
async def fetch_user_by_email(email):
    pool = await get_pool()



    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM users WHERE email = $1",
            email
        )

    

    if not row:
        return None

    return {
        "id": row["id"],
        "email": row["email"],
        "password": row["password"],
        "role": row["role"]
    }


