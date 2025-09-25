from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User

users_api = Blueprint('users_api', __name__)

@users_api.route('/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        'success': True,
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'is_admin': current_user.is_admin,
            'created_at': current_user.created_at.isoformat()
        }
    })

@users_api.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    if 'email' in data:
        if User.query.filter_by(email=data['email']).filter(User.id != current_user.id).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        current_user.email = data['email']
    
    if 'password' in data and data['password']:
        current_user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Profile updated successfully',
        'user': {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'is_admin': current_user.is_admin,
            'created_at': current_user.created_at.isoformat()
        }
    })

@users_api.route('/', methods=['GET'])
@login_required
def get_users():
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    users = User.query.all()
    
    return jsonify({
        'success': True,
        'users': [
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin,
                'created_at': user.created_at.isoformat()
            }
            for user in users
        ]
    })

@users_api.route('/', methods=['POST'])
def register_user():
    data = request.get_json()
    
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'success': False, 'error': 'Username, email, and password are required'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'success': False, 'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'success': False, 'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        is_admin=data.get('is_admin', False)
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User registered successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        }
    }), 201

@users_api.route('/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'No data provided'}), 400
    
    if 'email' in data:
        if User.query.filter_by(email=data['email']).filter(User.id != user_id).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        user.email = data['email']
    
    if 'is_admin' in data:
        user.is_admin = data['is_admin']
    
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin,
            'created_at': user.created_at.isoformat()
        }
    })

@users_api.route('/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'error': 'Admin privileges required'}), 403
    
    if user_id == current_user.id:
        return jsonify({'success': False, 'error': 'Cannot delete your own account'}), 400
    
    user = User.query.get_or_404(user_id)
    
    if user.uploaded_papers:
        return jsonify({
            'success': False, 
            'error': 'Cannot delete user with uploaded papers'
        }), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'User deleted successfully'
    })