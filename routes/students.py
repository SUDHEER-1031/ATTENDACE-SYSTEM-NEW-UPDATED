import shutil
from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from database.student_db import add_student, delete_student, get_student, list_students, update_student
from .auth import login_required

students_bp = Blueprint("students", __name__, url_prefix="/students")
def values(form): return tuple(form.get(x, "").strip() for x in ("roll_no", "name", "department", "email", "phone"))

@students_bp.get("/")
@login_required
def index(): return render_template("students.html", students=list_students(current_app.config["DATABASE"], request.args.get("q", "")), q=request.args.get("q", ""))

@students_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        try:
            student_id = add_student(current_app.config["DATABASE"], (*values(request.form), ""))
            flash("Student added. Capture face photos next.", "success")
            return redirect(url_for("camera.capture", student_id=student_id))
        except Exception as e: flash("Roll number already exists or required fields are missing.", "danger")
    return render_template("student_form.html", student=None)

@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit(student_id):
    student = get_student(current_app.config["DATABASE"], student_id)
    if not student: return redirect(url_for("students.index"))
    if request.method == "POST":
        try: update_student(current_app.config["DATABASE"], student_id, values(request.form)); flash("Student updated.", "success"); return redirect(url_for("students.index"))
        except Exception: flash("Could not save: roll number must be unique.", "danger")
    return render_template("student_form.html", student=student)

@students_bp.post("/<int:student_id>/delete")
@login_required
def delete(student_id):
    student = get_student(current_app.config["DATABASE"], student_id)
    if student:
        folder = current_app.config["DATASET_DIR"] / str(student_id)
        if folder.exists(): shutil.rmtree(folder)
        delete_student(current_app.config["DATABASE"], student_id); flash("Student removed.", "success")
    return redirect(url_for("students.index"))
