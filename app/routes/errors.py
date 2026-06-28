"""Error handling routes."""
from flask import Blueprint, render_template, request, jsonify
from app.constants import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(400)
def handle_400(error):
    """Handle 400 Bad Request."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Bad request', 'status': 400}), 400
    return render_template('errors/400.html'), 400


@errors_bp.app_errorhandler(403)
def handle_403(error):
    """Handle 403 Forbidden."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Access forbidden', 'status': 403}), 403
    return render_template('errors/403.html'), 403


@errors_bp.app_errorhandler(404)
def handle_404(error):
    """Handle 404 Not Found."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Resource not found', 'status': 404}), 404
    return render_template('errors/404.html'), 404


@errors_bp.app_errorhandler(500)
def handle_500(error):
    """Handle 500 Internal Server Error."""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error', 'status': 500}), 500
    return render_template('errors/500.html'), 500
