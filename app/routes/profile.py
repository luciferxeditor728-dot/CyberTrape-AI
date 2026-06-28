"""User profile routes."""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.routes import profile_bp
from app.services.user_service import UserService
from app.utils.decorators import login_required as custom_login_required
from app.utils.logger import get_logger

logger = get_logger(__name__)


@profile_bp.route('/')
@custom_login_required
def view_profile():
    """View user profile."""
    return render_template('profile/profile.html', user=current_user)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@custom_login_required
def edit_profile():
    """Edit user profile."""
    if request.method == 'POST':
        UserService.update_user(
            current_user,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            phone=request.form.get('phone'),
            location=request.form.get('location'),
            bio=request.form.get('bio')
        )
        flash('Profile updated successfully', 'success')
        return redirect(url_for('profile.view_profile'))
    
    return render_template('profile/edit_profile.html', user=current_user)


@profile_bp.route('/change-password', methods=['GET', 'POST'])
@custom_login_required
def change_password():
    """Change password."""
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('New passwords do not match', 'error')
        else:
            success, message = UserService.change_password(current_user, old_password, new_password)
            if success:
                flash(message, 'success')
                return redirect(url_for('profile.view_profile'))
            else:
                flash(message, 'error')
    
    return render_template('profile/change_password.html')


@profile_bp.route('/security')
@custom_login_required
def security():
    """Security settings."""
    return render_template('profile/security.html', user=current_user)


@profile_bp.route('/sessions')
@custom_login_required
def sessions():
    """View active sessions."""
    from app.models import Session
    user_sessions = Session.query.filter_by(user_id=current_user.id, is_active=True).all()
    return render_template('profile/sessions.html', sessions=user_sessions)


@profile_bp.route('/preferences')
@custom_login_required
def preferences():
    """User preferences."""
    return render_template('profile/preferences.html', user=current_user)
