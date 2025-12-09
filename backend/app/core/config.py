import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Smart Attendance API"

# CORS origins
ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Env-based fake users for now (later replace with DB)
# TEACHER_EMAIL = os.getenv("TEACHER_EMAIL")
# TEACHER_PASSWORD = os.getenv("TEACHER_PASSWORD")
# STUDENT_EMAIL = os.getenv("STUDENT_EMAIL")
# STUDENT_PASSWORD = os.getenv("STUDENT_PASSWORD")

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
BACKEND_BASE_URL = os.getenv("BACKEND_BASE_URL")


def get_fake_users():
    return {
        TEACHER_EMAIL: {
            "password": TEACHER_PASSWORD,
            "role": "Teacher",
            "name": "Demo Teacher",
        },
        STUDENT_EMAIL: {
            "password": STUDENT_PASSWORD,
            "role": "Student",
            "name": "Demo Student",
        },
    }
