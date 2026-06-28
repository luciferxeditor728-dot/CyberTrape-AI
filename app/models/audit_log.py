"""Audit log model for system auditing."""
from app import db
from datetime import datetime
import uuid


class AuditLog(db.Model):
    """Audit log for system-wide activities."""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Who performed the action
    actor_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    actor = db.relationship('User', backref='audit_logs_created')
    
    # What action was performed
    action = db.Column(db.String(100), nullable=False, index=True)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.String(36), nullable=False)
    
    # Changes made
    changes = db.Column(db.JSON, nullable=True)
    
    # Audit context
    reason = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    session_id = db.Column(db.String(100), nullable=True)
    
    # Result
    result = db.Column(db.String(20), default='success')
    error_message = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<AuditLog {self.action} on {self.entity_type}>'
