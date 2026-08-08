from flask import Flask
from config import Config
from database.db import init_db
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.students import students_bp
from routes.camera import camera_bp
from routes.attendance import attendance_bp
from routes.reports import reports_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    for directory in (app.config["DATASET_DIR"], app.config["MODELS_DIR"]):
        directory.mkdir(parents=True, exist_ok=True)
    init_db(app.config["DATABASE"])
    for blueprint in (auth_bp, dashboard_bp, students_bp, camera_bp, attendance_bp, reports_bp):
        app.register_blueprint(blueprint)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
