import psycopg2
from psycopg2.extras import RealDictCursor
from .config import POSTGRES

# -----------------------------
# Database connection
# -----------------------------
def get_conn():
    return psycopg2.connect(
        host=POSTGRES["host"],
        port=POSTGRES["port"],
        user=POSTGRES["user"],
        password=POSTGRES["password"],
        dbname=POSTGRES["dbname"],
    )

# -----------------------------
# Create users table
# -----------------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        qdrant_id TEXT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(id),
        event_type TEXT CHECK (event_type IN ('ENTRY', 'EXIT')),
        score FLOAT,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✔ PostgreSQL tables ready.")


# -----------------------------
# Create new user (Signup)
# -----------------------------
def create_user(name: str, email: str, password_hash: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING id;",
        (name, email, password_hash),
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return user_id

# -----------------------------
# Get user by email (Login)
# -----------------------------
def get_user_by_email(email: str):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s;", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

# -----------------------------
# Update Qdrant ID after face registration
# -----------------------------
def update_user_qdrant_id(user_id: int, qdrant_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET qdrant_id = %s WHERE id = %s;",
        (qdrant_id, user_id),
    )
    conn.commit()
    cur.close()
    conn.close()



def get_last_event(user_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT event_type, created_at
        FROM attendance_logs
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        return row[0], row[1]  # event_type, time
    return None, None



def save_attendance(user_id, event_type, score):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO attendance_logs (user_id, event_type, score)
        VALUES (%s, %s, %s)
    """, (user_id, event_type, score))
    conn.commit()
    cur.close()
    conn.close()

