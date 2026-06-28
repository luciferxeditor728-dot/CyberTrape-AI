"""API routes package."""
from flask import Blueprint

# API Blueprints
api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api/v1/auth')
api_users_bp = Blueprint('api_users', __name__, url_prefix='/api/v1/users')
api_analytics_bp = Blueprint('api_analytics', __name__, url_prefix='/api/v1/analytics')
api_admin_bp = Blueprint('api_admin', __name__, url_prefix='/api/v1/admin')

from app.routes.api import auth, users, analytics, admin
