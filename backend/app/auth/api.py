from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app import db

auth_api_bp = Blueprint('auth_api', __name__)

@auth_api_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({
            'success': True,
            'message': 'Already logged in',
            'user': {
                'id': current_user.id,
                'username': current_user.username,
                'email': current_user.email,
                'role': current_user.role.value
            }
        })
    
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            'success': False,
            'message': 'Username and password are required'
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role.value,
                'student_profile': None,
                'lecturer_profile': None
            }
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Invalid username or password'
        }), 401

@auth_api_bp.route('/logout', methods=['POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({
            'success': True,
            'message': 'You have been logged out.'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'No user is currently logged in'
        }), 400

@auth_api_bp.route('/me', methods=['GET'])
def get_current_user():
    if current_user.is_authenticated:
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'role': current_user.role.value,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
            'last_login': current_user.last_login.isoformat() if current_user.last_login else None
        }
        
        # Add profile information based on role
        if current_user.role.value == 'student' and hasattr(current_user, 'student_profile'):
            if current_user.student_profile:
                user_data['student_profile'] = {
                    'id': current_user.student_profile.id,
                    'full_name': current_user.student_profile.full_name,
                    'registration_number': current_user.student_profile.registration_number,
                    'academic_year': current_user.student_profile.academic_year,
                    'faculty': current_user.student_profile.faculty,
                    'department': current_user.student_profile.department,
                    'contact_number': current_user.student_profile.contact_number,
                    'enrolled_date': current_user.student_profile.enrolled_date.isoformat() if current_user.student_profile.enrolled_date else None,
                    'can_upload': current_user.student_profile.can_upload
                }
        elif current_user.role.value == 'lecturer' and hasattr(current_user, 'lecturer_profile'):
            if current_user.lecturer_profile:
                user_data['lecturer_profile'] = {
                    'id': current_user.lecturer_profile.id,
                    'full_name': current_user.lecturer_profile.full_name,
                    'employee_id': current_user.lecturer_profile.employee_id,
                    'department': current_user.lecturer_profile.department,
                    'position': current_user.lecturer_profile.position.value,
                    'office_location': current_user.lecturer_profile.office_location,
                    'contact_number': current_user.lecturer_profile.contact_number,
                    'joined_date': current_user.lecturer_profile.joined_date.isoformat() if current_user.lecturer_profile.joined_date else None
                }
        
        return jsonify({
            'success': True,
            'user': user_data
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Not authenticated'
        }), 401
