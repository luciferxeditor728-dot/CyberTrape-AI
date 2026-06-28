"""User service."""
from app import db
from app.models import User, Role, Permission
from app.utils.logger import get_logger
from datetime import datetime

logger = get_logger(__name__)


class UserService:
    """User management service."""
    
    @staticmethod
    def get_user(user_id):
        """Get user by ID."""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username):
        """Get user by username."""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email."""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def list_users(page=1, per_page=20, active_only=True):
        """List users."""
        query = User.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        return query.paginate(page=page, per_page=per_page, error_out=False)
    
    @staticmethod
    def update_user(user, **kwargs):
        """Update user information."""
        for key, value in kwargs.items():
            if hasattr(user, key) and key not in ['id', 'created_at']:
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f'User updated: {user.username}')
        return user
    
    @staticmethod
    def change_password(user, old_password, new_password):
        """Change user password."""
        if not user.check_password(old_password):
            return False, 'Invalid current password'
        
        user.set_password(new_password)
        db.session.commit()
        
        logger.info(f'Password changed for user: {user.username}')
        return True, 'Password changed successfully'
    
    @staticmethod
    def assign_role(user, role):
        """Assign role to user."""
        user.role = role
        db.session.commit()
        
        logger.info(f'Role {role.name} assigned to user: {user.username}')
        return user
    
    @staticmethod
    def deactivate_user(user):
        """Deactivate user account."""
        user.is_active = False
        db.session.commit()
        
        logger.info(f'User deactivated: {user.username}')
        return user
    
    @staticmethod
    def activate_user(user):
        """Activate user account."""
        user.is_active = True
        db.session.commit()
        
        logger.info(f'User activated: {user.username}')
        return user
    
    @staticmethod
    def delete_user(user):
        """Delete user (soft delete)."""
        user.deleted_at = datetime.utcnow()
        user.is_active = False
        db.session.commit()
        
        logger.info(f'User deleted: {user.username}')
        return user
