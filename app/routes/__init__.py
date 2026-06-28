"""Routes package."""
from flask import Blueprint

# Web routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
users_bp = Blueprint('users', __name__, url_prefix='/users')
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
settings_bp = Blueprint('settings', __name__, url_prefix='/settings')
notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')

# API routes
api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/v1/auth')
api_users_bp = Blueprint('api_users', __name__, url_prefix='/api/v1/users')
api_analytics_bp = Blueprint('api_analytics', __name__, url_prefix='/api/v1/analytics')
api_admin_bp = Blueprint('api_admin', __name__, url_prefix='/api/v1/admin')

from app.routes import (
    auth,
    dashboard,
    users,
    profile,
    settings,
    notifications,
    admin,
    analytics,
)
from app.routes.api import auth as api_auth, users as api_users, analytics as api_analytics, admin as api_admin
