from flask import Blueprint, current_app, render_template
from database.attendance_db import dashboard_stats
from .auth import login_required

dashboard_bp = Blueprint("dashboard", __name__)
@dashboard_bp.get("/")
@login_required
def index():
    total, present, recent = dashboard_stats(current_app.config["DATABASE"])
    return render_template("dashboard.html", total=total, present=present, absent=max(total-present,0), percentage=round(present*100/total,1) if total else 0, recent=recent)
