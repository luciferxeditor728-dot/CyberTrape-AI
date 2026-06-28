"""Role model for role-based access control."""
from app import db
from datetime import datetime
import uuid


class Role(db.Model):
    """Role model for RBAC."""
    __tablename__ = 'roles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    
    # Role configuration
    is_system_role = db.Column(db.Boolean, default=False)  # System roles can't be deleted
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    permissions = db.relationship(
        'Permission',
        secondary='role_permissions',
        backref='roles',
        lazy='dynamic'
    )
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def add_permission(self, permission):
        """Add permission to role."""
        if not self.has_permission(permission):
            self.permissions.append(permission)
    
    def remove_permission(self, permission):
        """Remove permission from role."""
        if self.has_permission(permission):
            self.permissions.remove(permission)
    
    def has_permission(self, permission):
        """Check if role has permission."""
        return self.permissions.filter_by(id=permission.id).first() is not None
    
    def __repr__(self):
        return f'<Role {self.name}>'
