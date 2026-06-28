"""Admin model for administrators and their permissions."""
from app import db
from datetime import datetime
import uuid


class Admin(db.Model):
    """Admin model for extended admin functionality."""
    __tablename__ = 'admins'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    user = db.relationship('User', backref='admin_profile', foreign_keys=[user_id])
    
    # Admin settings
    can_manage_users = db.Column(db.Boolean, default=True)
    can_manage_honeypots = db.Column(db.Boolean, default=True)
    can_manage_alerts = db.Column(db.Boolean, default=True)
    can_manage_admins = db.Column(db.Boolean, default=False)
    can_view_analytics = db.Column(db.Boolean, default=True)
    can_manage_backups = db.Column(db.Boolean, default=True)
    can_view_audit_logs = db.Column(db.Boolean, default=True)
    
    # Admin info
    promoted_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    promoted_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Admin {self.user.username}>'
