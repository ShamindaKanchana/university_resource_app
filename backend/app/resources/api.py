from flask import Blueprint, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.utils.decorators import student_required, upload_permission_required
from app.models import Resource, Category, ResourceDownload
from app import db
from datetime import datetime
import os

resources_api_bp = Blueprint('resources_api', __name__)

@resources_api_bp.route('/upload', methods=['POST'])
@login_required
@student_required
@upload_permission_required
def upload():
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Get form data
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category')
        
        if not all([title, category_id]):
            return jsonify({
                'success': False,
                'message': 'Title and category are required'
            }), 400
        
        # Validate category
        category = Category.query.get(category_id)
        if not category or not category.is_active:
            return jsonify({
                'success': False,
                'message': 'Invalid category'
            }), 400
        
        # Save file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Ensure upload directory exists
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(file_path)
        
        # Create resource record
        resource = Resource(
            title=title,
            description=description,
            category_id=category_id,
            uploaded_by_student_id=current_user.student_profile.id,
            file_path=file_path,
            file_name=filename,
            file_type=file.filename.rsplit('.', 1)[1].lower(),
            file_size=os.path.getsize(file_path)
        )
        
        db.session.add(resource)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Resource uploaded successfully! It will be reviewed by a lecturer.',
            'data': {
                'id': resource.id,
                'title': resource.title,
                'description': resource.description,
                'file_name': resource.file_name,
                'file_type': resource.file_type,
                'file_size': resource.file_size,
                'upload_date': resource.upload_date.isoformat(),
                'status': resource.status.value,
                'category': {
                    'id': category.id,
                    'name': category.name
                }
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error uploading resource: {str(e)}'
        }), 500

@resources_api_bp.route('/download/<int:resource_id>', methods=['GET'])
@login_required
def download(resource_id):
    try:
        resource = Resource.query.get_or_404(resource_id)
        
        if resource.status != 'approved':
            return jsonify({
                'success': False,
                'message': 'This resource is not available for download'
            }), 403
        
        # Log the download
        download_log = ResourceDownload(
            resource_id=resource_id,
            user_id=current_user.id,
            ip_address=request.remote_addr
        )
        db.session.add(download_log)
        
        # Increment download count
        resource.download_count += 1
        db.session.commit()
        
        return send_file(resource.file_path, as_attachment=True, download_name=resource.file_name)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error downloading resource: {str(e)}'
        }), 500

@resources_api_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    try:
        categories = Category.query.filter_by(is_active=True).all()
        
        categories_data = [{
            'id': c.id,
            'name': c.name,
            'description': c.description,
            'created_at': c.created_at.isoformat() if c.created_at else None
        } for c in categories]
        
        return jsonify({
            'success': True,
            'data': categories_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching categories: {str(e)}'
        }), 500

@resources_api_bp.route('/my-uploads', methods=['GET'])
@login_required
@student_required
def my_uploads():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status', '')
        
        # Build query
        query = Resource.query.filter_by(uploaded_by_student_id=current_user.student_profile.id)
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        # Paginate
        resources = query.order_by(Resource.upload_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        resources_data = [{
            'id': r.id,
            'title': r.title,
            'description': r.description,
            'file_name': r.file_name,
            'file_type': r.file_type,
            'file_size': r.file_size,
            'upload_date': r.upload_date.isoformat(),
            'status': r.status.value,
            'download_count': r.download_count,
            'review_date': r.review_date.isoformat() if r.review_date else None,
            'review_comments': r.review_comments,
            'rejection_reason': r.rejection_reason,
            'category': {
                'id': r.category.id,
                'name': r.category.name
            } if r.category else None
        } for r in resources.items]
        
        return jsonify({
            'success': True,
            'data': {
                'resources': resources_data,
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
            'message': f'Error fetching uploads: {str(e)}'
        }), 500
