"""Session model for session management."""
from app import db
from datetime import datetime, timedelta
import uuid
import secrets


class Session(db.Model):
    """Session model for user session tracking."""
    __tablename__ = 'sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    user = db.relationship('User', backref='sessions')
    
    # Session token
    token = db.Column(db.String(500), unique=True, nullable=False, index=True)
    
    # Session information
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.Text, nullable=True)
    device_name = db.Column(db.String(255), nullable=True)
    device_type = db.Column(db.String(50), nullable=True)
    os = db.Column(db.String(100), nullable=True)
    browser = db.Column(db.String(100), nullable=True)
    
    # Session status
    is_active = db.Column(db.Boolean, default=True)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Session lifecycle
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=True)
    
    @classmethod
    def create_session(cls, user_id, ip_address, user_agent=None, **kwargs):
        """Create a new session."""
        session = cls(
            user_id=user_id,
            token=secrets.token_urlsafe(64),
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=datetime.utcnow() + timedelta(days=7),
            **kwargs
        )
        return session
    
    def revoke(self):
        """Revoke session."""
        self.is_active = False
        self.revoked_at = datetime.utcnow()
    
    def is_valid(self):
        """Check if session is still valid."""
        return (
            self.is_active and
            self.expires_at > datetime.utcnow() and
            self.revoked_at is None
        )
    
    def __repr__(self):
        return f'<Session {self.user.username} from {self.ip_address}>'
