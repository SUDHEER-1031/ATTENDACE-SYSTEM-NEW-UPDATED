from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", BASE_DIR))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-before-deployment")
    DATABASE = DATA_DIR / "attendance.db"
    DATASET_DIR = DATA_DIR / "dataset"
    MODELS_DIR = DATA_DIR / "models"
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
