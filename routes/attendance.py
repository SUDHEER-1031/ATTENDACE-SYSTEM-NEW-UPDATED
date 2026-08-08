from datetime import date
from flask import Blueprint, current_app, render_template, request
from database.attendance_db import attendance_rows
from .auth import login_required
attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")
@attendance_bp.get("/")
@login_required
def index():
    chosen = request.args.get("date", date.today().isoformat())
    return render_template("attendance.html", rows=attendance_rows(current_app.config["DATABASE"], chosen), chosen=chosen)
