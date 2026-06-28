"""Notification model for user notifications."""
from app import db
from datetime import datetime
import uuid


class Notification(db.Model):
    """Notification model for user notifications."""
    __tablename__ = 'notifications'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='notifications')
    
    # Notification content
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(20), nullable=False)
    
    # Notification metadata
    related_entity_type = db.Column(db.String(50), nullable=True)
    related_entity_id = db.Column(db.String(36), nullable=True)
    
    # Notification delivery
    is_read = db.Column(db.Boolean, default=False, index=True)
    read_at = db.Column(db.DateTime, nullable=True)
    
    # Channels
    channels = db.Column(db.JSON, default=[])
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Notification {self.title} to {self.user.username}>'
