from datetime import date, datetime
from .db import get_connection

def mark_present(database, student_id):
    today = date.today().isoformat()
    with get_connection(database) as c:
        cur = c.execute("INSERT OR IGNORE INTO attendance (student_id,attendance_date,attendance_time,status) VALUES (?,?,?,?)",
              (student_id, today, datetime.now().strftime("%H:%M:%S"), "Present"))
        return cur.rowcount == 1

def attendance_rows(database, selected_date=""):
    with get_connection(database) as c:
        q = "SELECT a.*,s.roll_no,s.name,s.department FROM attendance a JOIN students s ON s.id=a.student_id"
        args = []
        if selected_date:
            q += " WHERE a.attendance_date=?"; args.append(selected_date)
        return c.execute(q + " ORDER BY a.attendance_date DESC,a.attendance_time DESC", args).fetchall()

def dashboard_stats(database):
    today = date.today().isoformat()
    with get_connection(database) as c:
        total = c.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        present = c.execute("SELECT COUNT(*) FROM attendance WHERE attendance_date=?", (today,)).fetchone()[0]
        recent = c.execute("SELECT a.*,s.name,s.roll_no FROM attendance a JOIN students s ON s.id=a.student_id ORDER BY a.id DESC LIMIT 6").fetchall()
    return total, present, recent
