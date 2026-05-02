from app.database import get_connection
from app.utils.security import hash_password
#  Create User
def create_user_service(user):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, email, age, city) VALUES (%s, %s, %s, %s)",
        (user.name, user.email, user.age, user.city)
    )

    conn.commit()
    cur.close()
    conn.close()


#  Fetch All Users
def fetch_all_users():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


#  Fetch User by ID
def fetch_user_by_id(user_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row

#Fetch user by email
def fetch_user_by_email(email: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    return row




def create_user_service(user):
    conn = get_connection()
    cur = conn.cursor()

    hashed_pwd = hash_password(user.password)

    cur.execute(
        "INSERT INTO users (name, email, age, city, password) VALUES (%s, %s, %s, %s, %s)",
        (user.name, user.email, user.age, user.city, hashed_pwd )
    )

    conn.commit()
    cur.close()
    conn.close()