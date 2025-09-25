import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app, create_admin_user, create_default_courses
from backend.models import db

def init_database():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_default_courses()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()