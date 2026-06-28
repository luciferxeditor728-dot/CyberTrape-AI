"""Activity log model for tracking user activities."""
from app import db
from datetime import datetime
import uuid


class ActivityLog(db.Model):
    """Activity log for user actions."""
    __tablename__ = 'activity_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='activity_logs')
    
    # Activity information
    activity_type = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    resource_type = db.Column(db.String(50), nullable=True)
    resource_id = db.Column(db.String(36), nullable=True)
    
    # Request information
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.Text, nullable=True)
    endpoint = db.Column(db.String(255), nullable=True)
    method = db.Column(db.String(10), nullable=True)
    
    # Activity outcome
    status = db.Column(db.String(20), nullable=True)
    status_code = db.Column(db.Integer, nullable=True)
    
    # Additional metadata
    metadata = db.Column(db.JSON, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<ActivityLog {self.activity_type} by {self.user.username}>'
