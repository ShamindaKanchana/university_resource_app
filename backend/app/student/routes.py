from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.decorators import student_required
from app.models import Resource, Category

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    # Get student's uploaded resources
    uploaded_resources = Resource.query.filter_by(
        uploaded_by_student_id=current_user.student_profile.id
    ).order_by(Resource.upload_date.desc()).limit(5).all()
    
    # Get recent approved resources
    recent_resources = Resource.query.filter_by(
        status='approved'
    ).order_by(Resource.upload_date.desc()).limit(10).all()
    
    return render_template('student/dashboard.html', 
                         uploaded_resources=uploaded_resources,
                         recent_resources=recent_resources)

@student_bp.route('/browse')
@login_required
@student_required
def browse():
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    
    query = Resource.query.filter_by(status='approved')
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    resources = query.order_by(Resource.upload_date.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('student/browse.html', 
                         resources=resources, 
                         categories=categories)
