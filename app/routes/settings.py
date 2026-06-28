"""Settings routes."""
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from app.routes import settings_bp
from app.utils.decorators import login_required as custom_login_required
from app.utils.logger import get_logger

logger = get_logger(__name__)


@settings_bp.route('/general')
@custom_login_required
def general():
    """General settings."""
    return render_template('settings/general.html')


@settings_bp.route('/security')
@custom_login_required
def security():
    """Security settings."""
    return render_template('settings/security.html')


@settings_bp.route('/notifications')
@custom_login_required
def notifications():
    """Notification settings."""
    return render_template('settings/notifications.html')


@settings_bp.route('/email')
@custom_login_required
def email():
    """Email settings."""
    return render_template('settings/email.html')


@settings_bp.route('/integrations')
@custom_login_required
def integrations():
    """Integration settings."""
    return render_template('settings/integrations.html')


@settings_bp.route('/advanced')
@custom_login_required
def advanced():
    """Advanced settings."""
    return render_template('settings/advanced.html')
