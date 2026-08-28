import base64
from pathlib import Path
from flask import Blueprint, current_app, jsonify, render_template, request
from database.student_db import get_student
from services.training_service import train_encodings
from services.recognition_service import recognize_image
from database.attendance_db import mark_present
from .auth import login_required

camera_bp = Blueprint("camera", __name__, url_prefix="/camera")
@camera_bp.get("/capture/<int:student_id>")
@login_required
def capture(student_id):
    student = get_student(current_app.config["DATABASE"], student_id)
    if not student:
        return "Student not found", 404
    return render_template("capture.html", student=student)

@camera_bp.post("/capture/<int:student_id>/save")
@login_required
def save_capture(student_id):
    if not get_student(current_app.config["DATABASE"], student_id):
        return jsonify(error="Student not found"), 404
    raw = (request.get_json(silent=True) or {}).get("image", "")
    if "," not in raw: return jsonify(error="No image received"), 400
    folder = Path(current_app.config["DATASET_DIR"]) / str(student_id); folder.mkdir(parents=True, exist_ok=True)
    number = len(list(folder.glob("*.jpg"))) + 1
    try:
        image_bytes = base64.b64decode(raw.split(",", 1)[1], validate=True)
    except (ValueError, TypeError):
        return jsonify(error="Invalid image data"), 400
    (folder / f"face_{number:03}.jpg").write_bytes(image_bytes)
    return jsonify(saved=number)

@camera_bp.route("/train", methods=["GET", "POST"])
@login_required
def train():
    result = None
    if request.method == "POST": result = train_encodings(current_app.config["DATABASE"], current_app.config["DATASET_DIR"], current_app.config["MODELS_DIR"])
    return render_template("train.html", result=result)

@camera_bp.get("/live")
@login_required
def live(): return render_template("live.html")

@camera_bp.post("/recognize")
@login_required
def recognize():
    raw = (request.get_json(silent=True) or {}).get("image", "")
    try:
        outcome = recognize_image(raw, current_app.config["MODELS_DIR"])
        if outcome.get("student_id"):
            outcome["marked"] = mark_present(current_app.config["DATABASE"], outcome["student_id"])
        return jsonify(outcome)
    except Exception as e: return jsonify(error=str(e)), 400
