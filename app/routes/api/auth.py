"""API authentication routes."""
from flask import request, jsonify
from app.routes import api_auth_bp
from app.services.auth_service import AuthService
from app.utils.helpers import get_client_ip
from app.utils.logger import get_logger
from app.constants import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_201_CREATED

logger = get_logger(__name__)


@api_auth_bp.route('/login', methods=['POST'])
def api_login():
    """API login endpoint."""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), HTTP_400_BAD_REQUEST
    
    user, error = AuthService.login(data['username'], data['password'], get_client_ip())
    
    if user:
        tokens = AuthService.generate_tokens(user)
        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': tokens
        }), HTTP_200_OK
    else:
        return jsonify({'error': error or 'Invalid credentials'}), HTTP_401_UNAUTHORIZED


@api_auth_bp.route('/register', methods=['POST'])
def api_register():
    """API registration endpoint."""
    data = request.get_json()
    
    required_fields = ['username', 'email', 'password']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST
    
    user, error = AuthService.register(
        data['username'],
        data['email'],
        data['password'],
        data.get('first_name'),
        data.get('last_name')
    )
    
    if user:
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        }), HTTP_201_CREATED
    else:
        return jsonify({'error': error or 'Registration failed'}), HTTP_400_BAD_REQUEST


@api_auth_bp.route('/logout', methods=['POST'])
def api_logout():
    """API logout endpoint."""
    return jsonify({'success': True, 'message': 'Logged out successfully'}), HTTP_200_OK
