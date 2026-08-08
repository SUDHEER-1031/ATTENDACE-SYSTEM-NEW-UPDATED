from functools import wraps
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from database.db import get_connection

auth_bp = Blueprint("auth", __name__)

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "admin_id" not in session:
            flash("Please sign in first.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username, password = request.form.get("username", ""), request.form.get("password", "")
        with get_connection(current_app.config["DATABASE"]) as c:
            admin = c.execute("SELECT * FROM admins WHERE username=?", (username,)).fetchone()
        if admin and check_password_hash(admin["password_hash"], password):
            session.clear(); session["admin_id"] = admin["id"]; session["username"] = admin["username"]
            return redirect(url_for("dashboard.index"))
        flash("Invalid username or password.", "danger")
    return render_template("login.html")

@auth_bp.get("/logout")
def logout():
    session.clear(); flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))
