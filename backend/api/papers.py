from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from models import db, QuestionPaper, Course

papers_api = Blueprint('papers_api', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@papers_api.route('/', methods=['GET'])
def get_papers():
    course_id = request.args.get('course_id')
    year = request.args.get('year')
    semester = request.args.get('semester')
    
    query = QuestionPaper.query
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    if year:
        query = query.filter_by(year=year)
    if semester:
        query = query.filter_by(semester=semester)
    
    papers = query.order_by(QuestionPaper.year.desc(), QuestionPaper.semester).all()
    
    return jsonify({
        'success': True,
        'papers': [
            {
                'id': paper.id,
                'title': paper.title,
                'course': {
                    'id': paper.course.id,
                    'name': paper.course.name,
                    'code': paper.course.code
                },
                'year': paper.year,
                'semester': paper.semester,
                'subject': paper.subject,
                'filename': paper.filename,
                'uploaded_by': paper.uploader.username,
                'created_at': paper.created_at.isoformat()
            }
            for paper in papers
        ]
    })

@papers_api.route('/<int:paper_id>', methods=['GET'])
def get_paper(paper_id):
    paper = QuestionPaper.query.get_or_404(paper_id)
    
    return jsonify({
        'success': True,
        'paper': {
            'id': paper.id,
            'title': paper.title,
            'course': {
                'id': paper.course.id,
                'name': paper.course.name,
                'code': paper.course.code
            },
            'year': paper.year,
            'semester': paper.semester,
            'subject': paper.subject,
            'filename': paper.filename,
            'uploaded_by': paper.uploader.username,
            'created_at': paper.created_at.isoformat()
        }
    })

@papers_api.route('/', methods=['POST'])
@login_required
def upload_paper():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Only PDF, DOC, and DOCX files are allowed.'}), 400
    
    title = request.form.get('title')
    course_id = request.form.get('course_id')
    year = request.form.get('year')
    semester = request.form.get('semester')
    subject = request.form.get('subject')
    
    if not all([title, course_id, year, semester, subject]):
        return jsonify({'success': False, 'error': 'All fields are required'}), 400
    
    try:
        year = int(year)
        semester = int(semester)
        course_id = int(course_id)
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid year, semester, or course_id'}), 400
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'success': False, 'error': 'Course not found'}), 404
    
    filename = secure_filename(file.filename)
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
    
    return jsonify({
        'success': True,
        'message': 'Question paper uploaded successfully',
        'paper': {
            'id': paper.id,
            'title': paper.title,
            'course': {
                'id': paper.course.id,
                'name': paper.course.name,
                'code': paper.course.code
            },
            'year': paper.year,
            'semester': paper.semester,
            'subject': paper.subject,
            'filename': paper.filename,
            'created_at': paper.created_at.isoformat()
        }
    }), 201

@papers_api.route('/<int:paper_id>', methods=['PUT'])
@login_required
def update_paper(paper_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    paper = QuestionPaper.query.get_or_404(paper_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    if 'title' in data:
        paper.title = data['title']
    if 'subject' in data:
        paper.subject = data['subject']
    if 'year' in data:
        paper.year = int(data['year'])
    if 'semester' in data:
        paper.semester = int(data['semester'])
    if 'course_id' in data:
        course = Course.query.get(data['course_id'])
        if not course:
            return jsonify({'success': False, 'error': 'Course not found'}), 404
        paper.course_id = data['course_id']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Question paper updated successfully',
        'paper': {
            'id': paper.id,
            'title': paper.title,
            'course': {
                'id': paper.course.id,
                'name': paper.course.name,
                'code': paper.course.code
            },
            'year': paper.year,
            'semester': paper.semester,
            'subject': paper.subject,
            'filename': paper.filename,
            'created_at': paper.created_at.isoformat()
        }
    })

@papers_api.route('/<int:paper_id>', methods=['DELETE'])
@login_required
def delete_paper(paper_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    paper = QuestionPaper.query.get_or_404(paper_id)
    
    try:
        os.remove(paper.file_path)
    except:
        pass
    
    db.session.delete(paper)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Question paper deleted successfully'
    })

@papers_api.route('/years', methods=['GET'])
def get_years():
    years = db.session.query(QuestionPaper.year).distinct().order_by(QuestionPaper.year.desc()).all()
    
    return jsonify({
        'success': True,
        'years': [year[0] for year in years]
    })

@papers_api.route('/subjects', methods=['GET'])
def get_subjects():
    course_id = request.args.get('course_id')
    year = request.args.get('year')
    semester = request.args.get('semester')
    
    query = db.session.query(QuestionPaper.subject)
    
    if course_id:
        query = query.filter_by(course_id=course_id)
    if year:
        query = query.filter_by(year=year)
    if semester:
        query = query.filter_by(semester=semester)
    
    subjects = query.distinct().all()
    
    return jsonify({
        'success': True,
        'subjects': [subject[0] for subject in subjects]
    })