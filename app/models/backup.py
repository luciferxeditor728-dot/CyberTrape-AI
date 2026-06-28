"""Backup model for system backups."""
from app import db
from datetime import datetime
import uuid


class Backup(db.Model):
    """Backup model for system backups."""
    __tablename__ = 'backups'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Backup information
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    backup_type = db.Column(db.String(50), nullable=False)
    
    # Backup target
    target_database = db.Column(db.String(100), nullable=False)
    backup_location = db.Column(db.String(500), nullable=False)
    
    # Backup metadata
    size_bytes = db.Column(db.BigInteger, nullable=True)
    compressed = db.Column(db.Boolean, default=True)
    encrypted = db.Column(db.Boolean, default=True)
    
    # Backup status
    status = db.Column(db.String(20), default='pending')
    progress = db.Column(db.Integer, default=0)
    error_message = db.Column(db.Text, nullable=True)
    
    # Backup creator
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    created_by_user = db.relationship('User', backref='backups_created')
    
    # Retention
    retention_days = db.Column(db.Integer, default=30)
    can_delete = db.Column(db.Boolean, default=True)
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Backup {self.name}>'
