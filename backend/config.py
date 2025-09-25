import os
from datetime import timedelta
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    BASE_DIR = Path(__file__).resolve().parent
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR / "question_papers.db"}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = BASE_DIR / 'frontend' / 'static' / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}