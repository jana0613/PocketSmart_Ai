import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from .config import get_settings

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

@contextmanager
def get_db():
    conn = sqlite3.connect(get_settings().database_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            planner TEXT NOT NULL,
            input_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        ''')

def create_user(email: str, password_hash: str):
    with get_db() as db:
        cur = db.execute("INSERT INTO users(email,password_hash,created_at) VALUES(?,?,?)", (email, password_hash, utc_now()))
        return cur.lastrowid

def get_user_by_email(email: str):
    with get_db() as db:
        return db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

def save_recommendation(user_id: int, planner: str, input_json: str, result_json: str):
    with get_db() as db:
        cur = db.execute("INSERT INTO recommendations(user_id,planner,input_json,result_json,created_at) VALUES(?,?,?,?,?)", (user_id, planner, input_json, result_json, utc_now()))
        return cur.lastrowid

def get_history(user_id: int, limit: int = 20):
    with get_db() as db:
        return db.execute("SELECT id,planner,input_json,result_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT ?", (user_id, limit)).fetchall()

def get_recommendation(user_id: int, rec_id: int):
    with get_db() as db:
        return db.execute("SELECT * FROM recommendations WHERE id=? AND user_id=?", (rec_id, user_id)).fetchone()
