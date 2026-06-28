"""Notifications routes."""
from flask import render_template, request, jsonify
from flask_login import current_user
from app.routes import notifications_bp
from app.models import Notification
from app.utils.decorators import login_required as custom_login_required
from app.utils.logger import get_logger
from app import db

logger = get_logger(__name__)


@notifications_bp.route('/center')
@custom_login_required
def center():
    """Notification center."""
    page = request.args.get('page', 1, type=int)
    notifications = Notification.query.filter_by(user_id=current_user.id).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('notifications/center.html', notifications=notifications)


@notifications_bp.route('/preferences')
@custom_login_required
def preferences():
    """Notification preferences."""
    return render_template('notifications/preferences.html')


@notifications_bp.route('/history')
@custom_login_required
def history():
    """Notification history."""
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(
        Notification.created_at.desc()
    ).limit(100).all()
    return render_template('notifications/history.html', notifications=notifications)


@notifications_bp.route('/<notification_id>/read', methods=['POST'])
@custom_login_required
def mark_read(notification_id):
    """Mark notification as read."""
    notification = Notification.query.get(notification_id)
    
    if notification and notification.user_id == current_user.id:
        notification.mark_as_read()
        db.session.commit()
        return jsonify({'success': True})
    
    return jsonify({'success': False}), 404
