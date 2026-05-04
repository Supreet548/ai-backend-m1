from app.database.connection import get_connection
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

    users = []

    for row in rows:
        users.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "age": row[4],
            "city": row[5],
            "role": row[6]
        })

    return users


#  Fetch User by ID
def fetch_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "age": row[4],
        "city": row[5],
        "role": row[6]
    }

#Fetch user by email
def fetch_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "email": row[2],
        "password": row[3],
        "role": row[6]
    }




def create_user_service(user):
    conn = get_connection()
    cur = conn.cursor()

    hashed_pwd = hash_password(user.password)

    cur.execute(
        "INSERT INTO users (name, email, age, city, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
        (user.name, user.email, user.age, user.city, hashed_pwd , user.role)
    )

    conn.commit()
    cur.close()
    conn.close()