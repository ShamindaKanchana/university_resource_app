from app import db
from sqlalchemy import Enum
import enum

class LecturerPosition(enum.Enum):
    professor = 'Professor'
    senior_lecturer = 'Senior Lecturer'
    lecturer = 'Lecturer'
    assistant_lecturer = 'Assistant Lecturer'
    visiting_lecturer = 'Visiting Lecturer'

class Lecturer(db.Model):
    __tablename__ = 'lecturers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    full_name = db.Column(db.String(100), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(Enum(LecturerPosition), nullable=False)
    office_location = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    joined_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
    # Relationships
    reviewed_resources = db.relationship('Resource', backref='lecturer_reviewer', lazy='dynamic')
    
    def __repr__(self):
        return f'<Lecturer {self.full_name} ({self.employee_id}) - {self.position.value}>'
