"""User management routes."""
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.routes import users_bp
from app.models import User
from app.services.user_service import UserService
from app.utils.decorators import admin_required
from app.utils.logger import get_logger

logger = get_logger(__name__)


@users_bp.route('/')
@admin_required
def list_users():
    """List all users."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = UserService.list_users(page=page, per_page=per_page)
    users = pagination.items
    
    return render_template('users/users_list.html', users=users, pagination=pagination)


@users_bp.route('/<user_id>')
@admin_required
def user_detail(user_id):
    """View user details."""
    user = UserService.get_user(user_id)
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('users.list_users'))
    
    return render_template('users/user_detail.html', user=user)


@users_bp.route('/<user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit user."""
    user = UserService.get_user(user_id)
    
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('users.list_users'))
    
    if request.method == 'POST':
        UserService.update_user(
            user,
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            location=request.form.get('location')
        )
        flash('User updated successfully', 'success')
        return redirect(url_for('users.user_detail', user_id=user.id))
    
    return render_template('users/user_edit.html', user=user)


@users_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user."""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user, error = AuthService.register(username, email, password)
        
        if user:
            flash('User created successfully', 'success')
            return redirect(url_for('users.user_detail', user_id=user.id))
        else:
            flash(error or 'Failed to create user', 'error')
    
    return render_template('users/user_create.html')


@users_bp.route('/<user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    """Deactivate user."""
    user = UserService.get_user(user_id)
    
    if user:
        UserService.deactivate_user(user)
        flash('User deactivated', 'success')
    else:
        flash('User not found', 'error')
    
    return redirect(url_for('users.list_users'))


@users_bp.route('/<user_id>/activate', methods=['POST'])
@admin_required
def activate_user(user_id):
    """Activate user."""
    user = UserService.get_user(user_id)
    
    if user:
        UserService.activate_user(user)
        flash('User activated', 'success')
    else:
        flash('User not found', 'error')
    
    return redirect(url_for('users.list_users'))
