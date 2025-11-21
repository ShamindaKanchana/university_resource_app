from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.decorators import lecturer_required
from app.models import Resource, Category
from datetime import datetime

lecturer_bp = Blueprint('lecturer', __name__)

@lecturer_bp.route('/dashboard')
@login_required
@lecturer_required
def dashboard():
    # Get pending resources for review
    pending_resources = Resource.query.filter_by(status='pending').order_by(Resource.upload_date.desc()).all()
    
    # Get resources reviewed by this lecturer
    reviewed_resources = Resource.query.filter_by(
        reviewed_by_lecturer_id=current_user.lecturer_profile.id
    ).order_by(Resource.review_date.desc()).limit(10).all()
    
    return render_template('lecturer/dashboard.html',
                         pending_resources=pending_resources,
                         reviewed_resources=reviewed_resources)

@lecturer_bp.route('/review/<int:resource_id>', methods=['GET', 'POST'])
@login_required
@lecturer_required
def review_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    
    if request.method == 'POST':
        action = request.form.get('action')
        comments = request.form.get('comments', '')
        
        if action == 'approve':
            resource.status = 'approved'
            resource.reviewed_by_lecturer_id = current_user.lecturer_profile.id
            resource.review_date = datetime.utcnow()
            resource.review_comments = comments
            flash('Resource approved successfully!', 'success')
        elif action == 'reject':
            resource.status = 'rejected'
            resource.reviewed_by_lecturer_id = current_user.lecturer_profile.id
            resource.review_date = datetime.utcnow()
            resource.review_comments = comments
            resource.rejection_reason = comments
            flash('Resource rejected.', 'info')
        
        db.session.commit()
        return redirect(url_for('lecturer.dashboard'))
    
    return render_template('lecturer/review.html', resource=resource)
