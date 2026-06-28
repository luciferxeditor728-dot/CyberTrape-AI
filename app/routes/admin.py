"""Admin routes."""
from flask import render_template, request, redirect, url_for, flash
from app.routes import admin_bp
from app.models import User, ActivityLog, AuditLog, Backup
from app.utils.decorators import admin_required
from app.utils.logger import get_logger

logger = get_logger(__name__)


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard."""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    recent_activity = ActivityLog.query.order_by(ActivityLog.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         active_users=active_users,
                         recent_activity=recent_activity)


@admin_bp.route('/logs')
@admin_required
def logs():
    """View system logs."""
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    return render_template('admin/logs.html', logs=logs)


@admin_bp.route('/backups')
@admin_required
def backups():
    """Manage backups."""
    page = request.args.get('page', 1, type=int)
    backups = Backup.query.order_by(Backup.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/backup.html', backups=backups)


@admin_bp.route('/api-keys')
@admin_required
def api_keys():
    """Manage API keys."""
    return render_template('admin/api_keys.html')


@admin_bp.route('/system-status')
@admin_required
def system_status():
    """System status."""
    return render_template('admin/system_status.html')
