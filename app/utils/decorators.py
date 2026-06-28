"""Decorators for routes and functions."""
from functools import wraps
from flask import request, jsonify, abort, current_app
from flask_login import current_user
from app.models import User, Permission, Role
from app.constants import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
import jwt
from datetime import datetime, timedelta


def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), HTTP_401_UNAUTHORIZED
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Unauthorized'}), HTTP_401_UNAUTHORIZED
            abort(401)
        
        if not current_user.role or current_user.role.name != 'admin':
            if request.path.startswith('/api/'):
                return jsonify({'error': 'Forbidden'}), HTTP_403_FORBIDDEN
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def permission_required(permission_name):
    """Decorator to check specific permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'Unauthorized'}), HTTP_401_UNAUTHORIZED
                abort(401)
            
            if not current_user.role:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'Forbidden'}), HTTP_403_FORBIDDEN
                abort(403)
            
            # Check if user has permission
            has_permission = False
            for perm in current_user.role.permissions:
                if perm.name == permission_name:
                    has_permission = True
                    break
            
            if not has_permission:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'Forbidden'}), HTTP_403_FORBIDDEN
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def token_required(f):
    """Decorator to validate JWT token for API endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), HTTP_401_UNAUTHORIZED
        
        if not token:
            return jsonify({'error': 'Token is missing'}), HTTP_401_UNAUTHORIZED
        
        try:
            data = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=[current_app.config['JWT_ALGORITHM']]
            )
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), HTTP_401_UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), HTTP_401_UNAUTHORIZED
        
        return f(*args, **kwargs)
    return decorated_function


def rate_limit(max_calls, time_period):
    """Decorator for rate limiting."""
    def decorator(f):
        calls = []
        
        @wraps(f)
        def decorated_function(*args, **kwargs):
            now = datetime.utcnow()
            calls_in_period = [c for c in calls if c > now - timedelta(seconds=time_period)]
            
            if len(calls_in_period) >= max_calls:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            calls.append(now)
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def async_task(f):
    """Decorator to run function as Celery task."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app.tasks.celery import app as celery_app
        return celery_app.task(f)(*args, **kwargs)
    return decorated_function
