import base64, pickle
from pathlib import Path
import numpy as np
import cv2

def recognize_image(data_url, models_dir):
    try: import face_recognition
    except ImportError: return {"student_id": None, "message": "Face recognition package is not installed."}
    model = Path(models_dir) / "encodings.pickle"
    if not model.exists(): return {"student_id": None, "message": "No trained model. Use Train Faces first."}
    raw = base64.b64decode(data_url.split(",", 1)[1]); image = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB); faces = face_recognition.face_encodings(rgb)
    if not faces: return {"student_id": None, "message": "No face detected. Face the camera and try again."}
    with open(model, "rb") as f: data = pickle.load(f)
    distances = face_recognition.face_distance(data["encodings"], faces[0])
    index = int(np.argmin(distances))
    if distances[index] > 0.48: return {"student_id": None, "message": "Face not recognized."}
    return {"student_id": data["student_ids"][index], "message": "Face recognized."}
