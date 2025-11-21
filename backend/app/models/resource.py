from app import db
from sqlalchemy import Enum
import enum
from datetime import datetime

class ResourceStatus(enum.Enum):
    pending = 'pending'
    approved = 'approved'
    rejected = 'rejected'

class Resource(db.Model):
    __tablename__ = 'resources'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    file_path = db.Column(db.String(500), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    upload_date = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(Enum(ResourceStatus), default=ResourceStatus.pending, nullable=False)
    download_count = db.Column(db.Integer, default=0)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    uploaded_by_student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    reviewed_by_lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    
    # Additional fields for review process
    review_date = db.Column(db.DateTime)
    review_comments = db.Column(db.Text)
    rejection_reason = db.Column(db.Text)
    
    # Relationships
    download_logs = db.relationship('ResourceDownload', backref='resource', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Resource {self.title} ({self.status.value})>'
