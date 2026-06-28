"""API admin routes."""
from flask import request, jsonify
from app.routes import api_admin_bp
from app.utils.decorators import token_required, admin_required
from app.utils.logger import get_logger
from app.constants import HTTP_200_OK

logger = get_logger(__name__)


@api_admin_bp.route('/stats', methods=['GET'])
@token_required
@admin_required
def stats():
    """Get admin statistics."""
    from app.models import User, ActivityLog, AuditLog
    
    return jsonify({
        'success': True,
        'stats': {
            'total_users': User.query.count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'total_activities': ActivityLog.query.count(),
            'total_audits': AuditLog.query.count(),
        }
    }), HTTP_200_OK


@api_admin_bp.route('/health', methods=['GET'])
@token_required
@admin_required
def health():
    """System health check."""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': __import__('datetime').datetime.utcnow().isoformat()
    }), HTTP_200_OK
