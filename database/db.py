import sqlite3
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash

def get_connection(database):
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db(database):
    Path(database).parent.mkdir(parents=True, exist_ok=True)
    with get_connection(database) as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT, roll_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL, department TEXT NOT NULL, email TEXT, phone TEXT,
            image_folder TEXT, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL, attendance_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Present',
            UNIQUE(student_id, attendance_date),
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );
        """)
        exists = conn.execute("SELECT 1 FROM admins WHERE username = ?", ("admin",)).fetchone()
        if not exists:
            conn.execute("INSERT INTO admins (username,password_hash,created_at) VALUES (?,?,?)",
                         ("admin", generate_password_hash("admin123"), datetime.now().isoformat(timespec="seconds")))
