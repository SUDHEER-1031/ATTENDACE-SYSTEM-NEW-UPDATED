# AI Face Recognition Attendance System

A final-year Flask web application for student records, webcam face capture, optional face recognition, automatic daily attendance, and Excel reports.

## Features

- Secure admin login and responsive blue dashboard
- Add, edit, search, and delete students
- Browser webcam capture (15–25 images per student recommended)
- Face-encoding training and live recognition with `face-recognition` (optional)
- One attendance entry per student per day
- Date-filtered attendance and Excel export

## Quick start

1. Open this folder in VS Code.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it (Windows): `.venv\Scripts\activate`
4. Install: `pip install -r requirements.txt`
5. For real matching, uncomment `face-recognition` in `requirements.txt`, then install again. This package may require CMake and Visual C++ Build Tools on Windows.
6. Start: `python app.py`
7. Open `http://127.0.0.1:5000`.

Default credentials are `admin` / `admin123`. Change the secret key and credentials before deployment.

## Recognition workflow

1. Add a student.
2. Capture several clear face images under even lighting.
3. Open **Train Faces** and train the encoding model.
4. Use **Live Attendance** to identify students and mark attendance.

Without the optional `face-recognition` package, all management, capture, database, and report features remain available; training and matching will explain what is missing instead of crashing.
