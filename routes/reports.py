from io import BytesIO
from flask import Blueprint, current_app, render_template, request, send_file
from database.attendance_db import attendance_rows
from .auth import login_required
reports_bp = Blueprint("reports", __name__, url_prefix="/reports")
@reports_bp.get("/")
@login_required
def index():
    chosen = request.args.get("date", "")
    return render_template("reports.html", rows=attendance_rows(current_app.config["DATABASE"], chosen), chosen=chosen)
@reports_bp.get("/export")
@login_required
def export():
    import pandas as pd
    rows = attendance_rows(current_app.config["DATABASE"], request.args.get("date", ""))
    data = [{"Roll No":r["roll_no"],"Name":r["name"],"Department":r["department"],"Date":r["attendance_date"],"Time":r["attendance_time"],"Status":r["status"]} for r in rows]
    out = BytesIO(); pd.DataFrame(data).to_excel(out, index=False); out.seek(0)
    return send_file(out, as_attachment=True, download_name="attendance_report.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
