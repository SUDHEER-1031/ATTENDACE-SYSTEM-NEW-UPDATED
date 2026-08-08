from datetime import datetime
from .db import get_connection

def list_students(database, search=""):
    with get_connection(database) as c:
        like = f"%{search.strip()}%"
        return c.execute("SELECT * FROM students WHERE roll_no LIKE ? OR name LIKE ? OR department LIKE ? ORDER BY name", (like, like, like)).fetchall()

def get_student(database, student_id):
    with get_connection(database) as c:
        return c.execute("SELECT * FROM students WHERE id=?", (student_id,)).fetchone()

def add_student(database, values):
    with get_connection(database) as c:
        cur = c.execute("INSERT INTO students (roll_no,name,department,email,phone,image_folder,created_at) VALUES (?,?,?,?,?,?,?)",
            (*values, datetime.now().isoformat(timespec="seconds")))
        return cur.lastrowid

def update_student(database, student_id, values):
    with get_connection(database) as c:
        c.execute("UPDATE students SET roll_no=?,name=?,department=?,email=?,phone=? WHERE id=?", (*values, student_id))

def delete_student(database, student_id):
    with get_connection(database) as c:
        c.execute("DELETE FROM students WHERE id=?", (student_id,))
