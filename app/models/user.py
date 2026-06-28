"""User model."""
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import uuid


class User(UserMixin, db.Model):
    """User model for authentication and management."""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_2fa_enabled = db.Column(db.Boolean, default=False, nullable=False)
    
    # 2FA secret
    totp_secret = db.Column(db.String(32), nullable=True)
    backup_codes = db.Column(db.JSON, nullable=True)
    
    # User metadata
    last_login = db.Column(db.DateTime, nullable=True)
    last_ip = db.Column(db.String(45), nullable=True)
    login_count = db.Column(db.Integer, default=0)
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    
    # Profile
    profile_image = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    location = db.Column(db.String(120), nullable=True)
    
    # Relationships
    role_id = db.Column(db.String(36), db.ForeignKey('roles.id'), nullable=True)
    role = db.relationship('Role', backref='users', lazy='joined')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Return user ID for Flask-Login."""
        return self.id
    
    @property
    def full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def __repr__(self):
        return f'<User {self.username}>'
