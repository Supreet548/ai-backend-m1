from app.database import get_connection

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