"""Analytics routes."""
from flask import render_template, request
from app.routes import analytics_bp
from app.utils.decorators import login_required as custom_login_required
from app.utils.logger import get_logger

logger = get_logger(__name__)


@analytics_bp.route('/')
@custom_login_required
def index():
    """Analytics dashboard."""
    return render_template('dashboard/analytics.html')


@analytics_bp.route('/attacks')
@custom_login_required
def attacks():
    """Attack analytics."""
    return render_template('dashboard/analytics.html')


@analytics_bp.route('/threats')
@custom_login_required
def threats():
    """Threat analytics."""
    return render_template('dashboard/analytics.html')


@analytics_bp.route('/trends')
@custom_login_required
def trends():
    """Trend analysis."""
    return render_template('dashboard/analytics.html')
