from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.utils.decorators import student_required, upload_permission_required
from app.models import Resource, Category, ResourceDownload
from app import db
from datetime import datetime
import os

resources_bp = Blueprint('resources', __name__)

@resources_bp.route('/upload', methods=['GET', 'POST'])
@login_required
@student_required
@upload_permission_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category')
        file = request.files.get('file')
        
        if not all([title, category_id, file]):
            flash('Please fill all required fields and select a file.', 'error')
            return redirect(request.url)
        
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
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
            
            flash('Resource uploaded successfully! It will be reviewed by a lecturer.', 'success')
            return redirect(url_for('student.dashboard'))
    
    categories = Category.query.filter_by(is_active=True).all()
    return render_template('resources/upload.html', categories=categories)

@resources_bp.route('/download/<int:resource_id>')
@login_required
def download(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    if resource.status != 'approved':
        flash('This resource is not available for download.', 'error')
        return redirect(url_for('student.browse'))
    
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
