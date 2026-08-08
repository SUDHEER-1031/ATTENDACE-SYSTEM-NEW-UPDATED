import pickle
from pathlib import Path
import cv2
import numpy as np

def train_encodings(database, dataset_dir, models_dir):
    """Create facial encodings. Install face-recognition for accurate matching."""
    try:
        import face_recognition
    except ImportError:
        return {"ok": False, "message": "Install the optional 'face-recognition' package to train real facial encodings."}
    encodings, ids, scanned = [], [], 0
    for folder in Path(dataset_dir).iterdir():
        if not folder.is_dir() or not folder.name.isdigit(): continue
        for image_path in folder.glob("*.jpg"):
            scanned += 1
            image = face_recognition.load_image_file(image_path)
            faces = face_recognition.face_encodings(image)
            if faces:
                encodings.append(faces[0]); ids.append(int(folder.name))
    if not encodings: return {"ok": False, "message": "No detectable faces found. Capture clear, front-facing photos first."}
    models_dir = Path(models_dir); models_dir.mkdir(parents=True, exist_ok=True)
    with open(models_dir / "encodings.pickle", "wb") as f: pickle.dump({"encodings": encodings, "student_ids": ids}, f)
    return {"ok": True, "message": f"Training complete: {len(encodings)} face samples from {len(set(ids))} student(s).", "samples": len(encodings)}
