from app import db
from datetime import datetime

class ResourceDownload(db.Model):
    __tablename__ = 'resource_downloads'
    
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    download_date = db.Column(db.DateTime, server_default=db.func.now())
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    
    # Relationships
    user = db.relationship('User', backref='download_logs')
    
    def __repr__(self):
        return f'<ResourceDownload Resource:{self.resource_id} User:{self.user_id}>'
