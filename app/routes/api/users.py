"""API user routes."""
from flask import request, jsonify
from app.routes import api_users_bp
from app.models import User
from app.services.user_service import UserService
from app.utils.decorators import token_required
from app.utils.logger import get_logger
from app.constants import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

logger = get_logger(__name__)


@api_users_bp.route('/', methods=['GET'])
@token_required
def get_users():
    """Get all users."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = UserService.list_users(page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'users': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
        } for user in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), HTTP_200_OK


@api_users_bp.route('/<user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    """Get user by ID."""
    user = UserService.get_user(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'created_at': user.created_at.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
        }
    }), HTTP_200_OK


@api_users_bp.route('/<user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    """Update user."""
    user = UserService.get_user(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    
    data = request.get_json()
    
    user = UserService.update_user(user, **data)
    
    return jsonify({
        'success': True,
        'message': 'User updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    }), HTTP_200_OK


@api_users_bp.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    """Delete user."""
    user = UserService.get_user(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND
    
    UserService.delete_user(user)
    
    return jsonify({'success': True, 'message': 'User deleted successfully'}), HTTP_200_OK
