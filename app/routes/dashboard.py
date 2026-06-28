"""Dashboard routes."""
from flask import render_template
from flask_login import login_required, current_user
from app.routes import dashboard_bp
from app.utils.decorators import login_required as custom_login_required
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dashboard_bp.route('/')
@custom_login_required
def index():
    """Dashboard home."""
    # Determine which dashboard to show based on user role
    if current_user.role and current_user.role.name == 'admin':
        return render_template('dashboard/admin_dashboard.html')
    else:
        return render_template('dashboard/user_dashboard.html')


@dashboard_bp.route('/overview')
@custom_login_required
def overview():
    """Dashboard overview."""
    return render_template('dashboard/overview.html')


@dashboard_bp.route('/analytics')
@custom_login_required
def analytics():
    """Analytics dashboard."""
    return render_template('dashboard/analytics.html')


@dashboard_bp.route('/activity')
@custom_login_required
def activity():
    """Activity feed."""
    return render_template('dashboard/activity_feed.html')
