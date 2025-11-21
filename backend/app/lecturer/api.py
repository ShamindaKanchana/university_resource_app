from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.utils.decorators import lecturer_required
from app.models import Resource, Category
from app import db
from datetime import datetime

lecturer_api_bp = Blueprint('lecturer_api', __name__)

@lecturer_api_bp.route('/dashboard', methods=['GET'])
@login_required
@lecturer_required
def dashboard():
    try:
        # Get pending resources for review
        pending_resources = Resource.query.filter_by(status='pending').order_by(Resource.upload_date.desc()).all()
        
        # Get resources reviewed by this lecturer
        reviewed_resources = Resource.query.filter_by(
            reviewed_by_lecturer_id=current_user.lecturer_profile.id
        ).order_by(Resource.review_date.desc()).limit(10).all()
        
        pending_data = [{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file_name': r.file_name,
            'file_type': r.file_type,
            'file_size': r.file_size,
            'upload_date': r.upload_date.isoformat(),
            'category': {
                'id': r.category.id,
                'name': r.category.name
            } if r.category else None,
            'uploader': {
                'full_name': r.student_uploader.full_name if r.student_uploader else 'Unknown',
                'registration_number': r.student_uploader.registration_number if r.student_uploader else 'Unknown'
            } if r.student_uploader else None
        } for r in pending_resources]
        
        reviewed_data = [{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file_name': r.file_name,
            'file_type': r.file_type,
            'file_size': r.file_size,
            'upload_date': r.upload_date.isoformat(),
            'status': r.status.value,
            'review_date': r.review_date.isoformat() if r.review_date else None,
            'review_comments': r.review_comments,
            'rejection_reason': r.rejection_reason,
            'category': {
                'id': r.category.id,
                'name': r.category.name
            } if r.category else None,
            'uploader': {
                'full_name': r.student_uploader.full_name if r.student_uploader else 'Unknown',
                'registration_number': r.student_uploader.registration_number if r.student_uploader else 'Unknown'
            } if r.student_uploader else None
        } for r in reviewed_resources]
        
        return jsonify({
            'success': True,
            'data': {
                'pending_resources': pending_data,
                'reviewed_resources': reviewed_data,
                'lecturer_info': {
                    'full_name': current_user.lecturer_profile.full_name,
                    'employee_id': current_user.lecturer_profile.employee_id,
                    'position': current_user.lecturer_profile.position.value,
                    'department': current_user.lecturer_profile.department
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching dashboard data: {str(e)}'
        }), 500

@lecturer_api_bp.route('/review/<int:resource_id>', methods=['GET'])
@login_required
@lecturer_required
def get_resource_for_review(resource_id):
    try:
        resource = Resource.query.get_or_404(resource_id)
        
        resource_data = {
            'id': resource.id,
            'title': resource.title,
            'description': resource.description,
            'file_name': resource.file_name,
            'file_type': resource.file_type,
            'file_size': resource.file_size,
            'upload_date': resource.upload_date.isoformat(),
            'status': resource.status.value,
            'category': {
                'id': resource.category.id,
                'name': resource.category.name
            } if resource.category else None,
            'uploader': {
                'full_name': resource.student_uploader.full_name if resource.student_uploader else 'Unknown',
                'registration_number': resource.student_uploader.registration_number if resource.student_uploader else 'Unknown',
                'faculty': resource.student_uploader.faculty if resource.student_uploader else 'Unknown',
                'department': resource.student_uploader.department if resource.student_uploader else 'Unknown'
            } if resource.student_uploader else None
        }
        
        return jsonify({
            'success': True,
            'data': resource_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching resource: {str(e)}'
        }), 500

@lecturer_api_bp.route('/review/<int:resource_id>', methods=['POST'])
@login_required
@lecturer_required
def review_resource(resource_id):
    try:
        resource = Resource.query.get_or_404(resource_id)
        data = request.get_json()
        
        if not data or 'action' not in data:
            return jsonify({
                'success': False,
                'message': 'Action is required (approve/reject)'
            }), 400
        
        action = data.get('action')
        comments = data.get('comments', '')
        
        if action == 'approve':
            resource.status = 'approved'
            resource.reviewed_by_lecturer_id = current_user.lecturer_profile.id
            resource.review_date = datetime.utcnow()
            resource.review_comments = comments
            resource.rejection_reason = None
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Resource approved successfully!',
                'data': {
                    'id': resource.id,
                    'status': resource.status.value,
                    'review_date': resource.review_date.isoformat()
                }
            })
            
        elif action == 'reject':
            resource.status = 'rejected'
            resource.reviewed_by_lecturer_id = current_user.lecturer_profile.id
            resource.review_date = datetime.utcnow()
            resource.review_comments = comments
            resource.rejection_reason = comments
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Resource rejected.',
                'data': {
                    'id': resource.id,
                    'status': resource.status.value,
                    'review_date': resource.review_date.isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid action. Must be approve or reject.'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error reviewing resource: {str(e)}'
        }), 500

@lecturer_api_bp.route('/profile', methods=['GET'])
@login_required
@lecturer_required
def profile():
    try:
        profile_data = {
            'id': current_user.lecturer_profile.id,
            'full_name': current_user.lecturer_profile.full_name,
            'employee_id': current_user.lecturer_profile.employee_id,
            'department': current_user.lecturer_profile.department,
            'position': current_user.lecturer_profile.position.value,
            'office_location': current_user.lecturer_profile.office_location,
            'contact_number': current_user.lecturer_profile.contact_number,
            'joined_date': current_user.lecturer_profile.joined_date.isoformat() if current_user.lecturer_profile.joined_date else None,
            'is_active': current_user.lecturer_profile.is_active,
            'created_at': current_user.lecturer_profile.created_at.isoformat() if current_user.lecturer_profile.created_at else None
        }
        
        return jsonify({
            'success': True,
            'data': profile_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching profile: {str(e)}'
        }), 500
