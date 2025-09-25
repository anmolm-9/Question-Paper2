from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db, Course, QuestionPaper

admin_bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('main.home'))
    
    courses = Course.query.all()
    papers = QuestionPaper.query.order_by(QuestionPaper.created_at.desc()).all()
    return render_template('admin.html', courses=courses, papers=papers)

@admin_bp.route('/add-course', methods=['POST'])
@login_required
def add_course():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('main.home'))
    
    name = request.form['name']
    code = request.form['code']
    
    if Course.query.filter_by(code=code).first():
        flash('Course code already exists')
        return redirect(url_for('admin.admin_panel'))
    
    course = Course(name=name, code=code)
    db.session.add(course)
    db.session.commit()
    flash('Course added successfully')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/upload-paper', methods=['POST'])
@login_required
def upload_paper():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('main.home'))
    
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('admin.admin_panel'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('admin.admin_panel'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        course_id = request.form['course_id']
        year = int(request.form['year'])
        semester = int(request.form['semester'])
        subject = request.form['subject']
        title = request.form['title']
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{year}_{semester}_{course_id}")
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        
        paper = QuestionPaper(
            title=title,
            course_id=course_id,
            year=year,
            semester=semester,
            subject=subject,
            filename=filename,
            file_path=file_path,
            uploaded_by=current_user.id
        )
        
        db.session.add(paper)
        db.session.commit()
        flash('Question paper uploaded successfully')
    else:
        flash('Invalid file type. Only PDF, DOC, and DOCX files are allowed.')
    
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/delete-paper/<int:paper_id>')
@login_required
def delete_paper(paper_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('main.home'))
    
    paper = QuestionPaper.query.get_or_404(paper_id)
    
    try:
        os.remove(paper.file_path)
    except:
        pass
    
    db.session.delete(paper)
    db.session.commit()
    flash('Question paper deleted successfully')
    return redirect(url_for('admin.admin_panel'))