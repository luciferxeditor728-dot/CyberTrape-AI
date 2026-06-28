"""API Key model for API authentication."""
from app import db
from datetime import datetime, timedelta
import uuid
import secrets
import hashlib


class APIKey(db.Model):
    """API Key model for programmatic access."""
    __tablename__ = 'api_keys'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='api_keys')
    
    # Key information
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    key_hash = db.Column(db.String(255), unique=True, nullable=False, index=True)
    key_preview = db.Column(db.String(20), nullable=False)
    
    # Key permissions/scopes
    scopes = db.Column(db.JSON, default=[])
    
    # Key status
    is_active = db.Column(db.Boolean, default=True)
    last_used_at = db.Column(db.DateTime, nullable=True)
    last_used_ip = db.Column(db.String(45), nullable=True)
    usage_count = db.Column(db.Integer, default=0)
    
    # Key lifecycle
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    revoked_at = db.Column(db.DateTime, nullable=True)
    
    @classmethod
    def create_key(cls, user_id, name, scopes=None):
        """Create a new API key."""
        raw_key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        
        api_key = cls(
            user_id=user_id,
            name=name,
            key_hash=key_hash,
            key_preview=raw_key[-20:],
            scopes=scopes or [],
            expires_at=datetime.utcnow() + timedelta(days=365)
        )
        
        return api_key, raw_key
    
    def is_valid(self):
        """Check if API key is still valid."""
        now = datetime.utcnow()
        return (
            self.is_active and
            (self.expires_at is None or self.expires_at > now) and
            self.revoked_at is None
        )
    
    def record_usage(self, ip_address):
        """Record API key usage."""
        self.last_used_at = datetime.utcnow()
        self.last_used_ip = ip_address
        self.usage_count += 1
    
    def revoke(self):
        """Revoke the API key."""
        self.is_active = False
        self.revoked_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<APIKey {self.name} for {self.user.username}>'
