"""Authentication service."""
from app import db
from app.models import User, ActivityLog
from app.utils.security import generate_jwt_token, verify_jwt_token, generate_totp_secret, verify_totp, hash_backup_codes
from app.utils.helpers import get_client_ip
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)


class AuthService:
    """Authentication service."""
    
    @staticmethod
    def login(username, password, ip_address):
        """Authenticate user."""
        user = User.query.filter_by(username=username).first()
        
        if not user:
            logger.warning(f'Login attempt with invalid username: {username}')
            return None, 'Invalid username or password'
        
        if not user.is_active:
            logger.warning(f'Login attempt by inactive user: {username}')
            return None, 'Account is inactive'
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            logger.warning(f'Login attempt to locked account: {username}')
            return None, 'Account is temporarily locked'
        
        # Check password
        if not user.check_password(password):
            user.failed_login_attempts += 1
            
            # Lock account after 5 failed attempts
            if user.failed_login_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)
                logger.warning(f'Account locked due to failed login attempts: {username}')
            
            db.session.commit()
            logger.warning(f'Login attempt with invalid password: {username}')
            return None, 'Invalid username or password'
        
        # Reset failed attempts
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        user.last_ip = ip_address
        user.login_count += 1
        
        db.session.commit()
        
        # Log activity
        activity = ActivityLog(
            user_id=user.id,
            activity_type='login',
            ip_address=ip_address,
            status='success'
        )
        db.session.add(activity)
        db.session.commit()
        
        logger.info(f'User logged in: {username}')
        return user, None
    
    @staticmethod
    def register(username, email, password, first_name=None, last_name=None):
        """Register new user."""
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return None, 'Username already exists'
        
        if User.query.filter_by(email=email).first():
            return None, 'Email already exists'
        
        # Create user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_verified=False
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        logger.info(f'New user registered: {username}')
        return user, None
    
    @staticmethod
    def enable_2fa(user):
        """Enable 2FA for user."""
        secret = generate_totp_secret()
        user.totp_secret = secret
        user.backup_codes = hash_backup_codes([])
        db.session.commit()
        
        logger.info(f'2FA enabled for user: {user.username}')
        return secret
    
    @staticmethod
    def verify_2fa(user, token):
        """Verify 2FA token."""
        if not user.totp_secret:
            return False
        
        return verify_totp(user.totp_secret, token)
    
    @staticmethod
    def generate_tokens(user):
        """Generate JWT tokens for user."""
        access_token = generate_jwt_token(user.id)
        
        # Generate refresh token (longer expiration)
        refresh_token = generate_jwt_token(
            user.id,
            expires_in=86400 * 30  # 30 days
        )
        
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'Bearer'
        }
