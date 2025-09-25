from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User
from pathlib import Path

def create_app():
    template_dir = Path(__file__).resolve().parent.parent / 'frontend' / 'templates'
    static_dir = Path(__file__).resolve().parent.parent / 'frontend' / 'static'

    app = Flask(__name__, 
                template_folder=str(template_dir),
                static_folder=str(static_dir))

    app.config.from_object(Config)

    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.admin import admin_bp
    from api.courses import courses_api
    from api.papers import papers_api
    from api.users import users_api

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(courses_api, url_prefix='/api/courses')
    app.register_blueprint(papers_api, url_prefix='/api/papers')
    app.register_blueprint(users_api, url_prefix='/api/users')

    return app

def create_admin_user():
    from werkzeug.security import generate_password_hash
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@questionpapers.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()

def create_default_courses():
    from models import Course
    courses_data = [
        {'name': 'Bachelor of Science in Computer Science', 'code': 'BSCCS'},
        {'name': 'Bachelor of Science in Information Technology', 'code': 'BSCIT'},
        {'name': 'Bachelor of Commerce', 'code': 'BCOM'}
    ]
    
    for course_data in courses_data:
        if not Course.query.filter_by(code=course_data['code']).first():
            course = Course(name=course_data['name'], code=course_data['code'])
            db.session.add(course)
    
    db.session.commit()

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        db.create_all()
        create_admin_user()
        create_default_courses()
    
    app.run(debug=True)