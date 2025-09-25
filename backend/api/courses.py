from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, Course

courses_api = Blueprint('courses_api', __name__)

@courses_api.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify({
        'success': True,
        'courses': [
            {
                'id': course.id,
                'name': course.name,
                'code': course.code,
                'created_at': course.created_at.isoformat()
            }
            for course in courses
        ]
    })

@courses_api.route('/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify({
        'success': True,
        'course': {
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'created_at': course.created_at.isoformat()
        }
    })

@courses_api.route('/', methods=['POST'])
@login_required
def create_course():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    data = request.get_json()
    
    if not data or 'name' not in data or 'code' not in data:
        return jsonify({'success': False, 'error': 'Name and code are required'}), 400
    
    if Course.query.filter_by(code=data['code']).first():
        return jsonify({'success': False, 'error': 'Course code already exists'}), 400
    
    course = Course(
        name=data['name'],
        code=data['code']
    )
    
    db.session.add(course)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Course created successfully',
        'course': {
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'created_at': course.created_at.isoformat()
        }
    }), 201

@courses_api.route('/<int:course_id>', methods=['PUT'])
@login_required
def update_course(course_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    course = Course.query.get_or_404(course_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    if 'name' in data:
        course.name = data['name']
    if 'code' in data:
        if Course.query.filter_by(code=data['code']).filter(Course.id != course_id).first():
            return jsonify({'success': False, 'error': 'Course code already exists'}), 400
        course.code = data['code']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Course updated successfully',
        'course': {
            'id': course.id,
            'name': course.name,
            'code': course.code,
            'created_at': course.created_at.isoformat()
        }
    })

@courses_api.route('/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    course = Course.query.get_or_404(course_id)
    
    if course.question_papers:
        return jsonify({
            'success': False, 
            'error': 'Cannot delete course with existing question papers'
        }), 400
    
    db.session.delete(course)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Course deleted successfully'
    })