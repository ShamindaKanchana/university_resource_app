from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.utils.decorators import student_required
from app.models import Resource, Category
from app import db

student_api_bp = Blueprint('student_api', __name__)

@student_api_bp.route('/dashboard', methods=['GET'])
@login_required
@student_required
def dashboard():
    try:
        # Get student's uploaded resources
        uploaded_resources = Resource.query.filter_by(
            uploaded_by_student_id=current_user.student_profile.id
        ).order_by(Resource.upload_date.desc()).limit(5).all()
        
        # Get recent approved resources
        recent_resources = Resource.query.filter_by(
            status='approved'
        ).order_by(Resource.upload_date.desc()).limit(10).all()
        
        uploaded_data = [{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file_name': r.file_name,
            'file_type': r.file_type,
            'file_size': r.file_size,
            'upload_date': r.upload_date.isoformat(),
            'status': r.status.value,
            'download_count': r.download_count,
            'category': {
                'id': r.category.id,
                'name': r.category.name
            } if r.category else None
        } for r in uploaded_resources]
        
        recent_data = [{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file_name': r.file_name,
            'file_type': r.file_type,
            'file_size': r.file_size,
            'upload_date': r.upload_date.isoformat(),
            'download_count': r.download_count,
            'category': {
                'id': r.category.id,
                'name': r.category.name
            } if r.category else None,
            'uploader': {
                'full_name': r.student_uploader.full_name if r.student_uploader else 'Unknown',
                'registration_number': r.student_uploader.registration_number if r.student_uploader else 'Unknown'
            } if r.student_uploader else None
        } for r in recent_resources]
        
        return jsonify({
            'success': True,
            'data': {
                'uploaded_resources': uploaded_data,
                'recent_resources': recent_data,
                'student_info': {
                    'full_name': current_user.student_profile.full_name,
                    'registration_number': current_user.student_profile.registration_number,
                    'can_upload': current_user.student_profile.can_upload
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching dashboard data: {str(e)}'
        }), 500

@student_api_bp.route('/browse', methods=['GET'])
@login_required
@student_required
def browse():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category_id = request.args.get('category', type=int)
        search = request.args.get('search', '')
        
        # Build query
        query = Resource.query.filter_by(status='approved')
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Resource.title.contains(search) | Resource.description.contains(search))
        
        # Paginate
        resources = query.order_by(Resource.upload_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # Get categories
        categories = Category.query.filter_by(is_active=True).all()
        
        resources_data = [{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file_name': r.file_name,
            'file_type': r.file_type,
            'file_size': r.file_size,
            'upload_date': r.upload_date.isoformat(),
            'download_count': r.download_count,
            'category': {
                'id': r.category.id,
                'name': r.category.name
            } if r.category else None,
            'uploader': {
                'full_name': r.student_uploader.full_name if r.student_uploader else 'Unknown',
                'registration_number': r.student_uploader.registration_number if r.student_uploader else 'Unknown'
            } if r.student_uploader else None
        } for r in resources.items]
        
        categories_data = [{
            'id': c.id,
            'name': c.name,
            'description': c.description
        } for c in categories]
        
        return jsonify({
            'success': True,
            'data': {
                'resources': resources_data,
                'categories': categories_data,
                'pagination': {
                    'page': resources.page,
                    'pages': resources.pages,
                    'per_page': resources.per_page,
                    'total': resources.total,
                    'has_next': resources.has_next,
                    'has_prev': resources.has_prev
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error browsing resources: {str(e)}'
        }), 500

@student_api_bp.route('/profile', methods=['GET'])
@login_required
@student_required
def profile():
    try:
        profile_data = {
            'id': current_user.student_profile.id,
            'full_name': current_user.student_profile.full_name,
            'registration_number': current_user.student_profile.registration_number,
            'academic_year': current_user.student_profile.academic_year,
            'faculty': current_user.student_profile.faculty,
            'department': current_user.student_profile.department,
            'contact_number': current_user.student_profile.contact_number,
            'enrolled_date': current_user.student_profile.enrolled_date.isoformat() if current_user.student_profile.enrolled_date else None,
            'can_upload': current_user.student_profile.can_upload,
            'is_active': current_user.student_profile.is_active,
            'created_at': current_user.student_profile.created_at.isoformat() if current_user.student_profile.created_at else None
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
