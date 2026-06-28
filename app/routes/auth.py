"""Authentication routes."""
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, current_user
from app.routes import auth_bp
from app.models import User
from app.services.auth_service import AuthService
from app.utils.validators import validate_email, validate_username, validate_password, ValidationError
from app.utils.helpers import get_client_ip
from app.utils.logger import get_logger
from app import db

logger = get_logger(__name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user, error = AuthService.login(username, password, get_client_ip())
        
        if user:
            if user.is_2fa_enabled:
                session['pending_user_id'] = user.id
                return redirect(url_for('auth.verify_2fa'))
            
            login_user(user, remember=remember)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash(error or 'Invalid credentials', 'error')
    
    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        try:
            validate_username(username)
            validate_email(email)
            validate_password(password, {'PASSWORD_MIN_LENGTH': 8})
            
            if password != confirm_password:
                raise ValidationError('Passwords do not match')
            
            user, error = AuthService.register(username, email, password, first_name, last_name)
            
            if user:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('auth.login'))
            else:
                flash(error or 'Registration failed', 'error')
        
        except ValidationError as e:
            flash(str(e), 'error')
    
    return render_template('auth/register.html')


@auth_bp.route('/logout')
def logout():
    """User logout route."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/2fa-setup')
def setup_2fa():
    """Setup 2FA route."""
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if current_user.is_2fa_enabled:
        flash('2FA is already enabled', 'info')
        return redirect(url_for('profile.security'))
    
    secret = AuthService.enable_2fa(current_user)
    
    import pyotp
    import qrcode
    from io import BytesIO
    import base64
    
    totp = pyotp.TOTP(secret)
    qr = qrcode.QRCode()
    qr.add_data(totp.provisioning_uri(current_user.email, issuer_name='CyberTrap-AI'))
    qr.make()
    
    img = qr.make_image()
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    qr_code = base64.b64encode(img_io.getvalue()).decode()
    
    return render_template('auth/2fa_setup.html', secret=secret, qr_code=qr_code)


@auth_bp.route('/verify-2fa', methods=['GET', 'POST'])
def verify_2fa():
    """Verify 2FA token."""
    if request.method == 'POST':
        token = request.form.get('token')
        pending_user_id = session.get('pending_user_id')
        
        if not pending_user_id:
            flash('Session expired', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.get(pending_user_id)
        
        if user and AuthService.verify_2fa(user, token):
            login_user(user)
            session.pop('pending_user_id', None)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid 2FA token', 'error')
    
    return render_template('auth/verify_2fa.html')


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password route."""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate reset token and send email
            flash('If an account exists with that email, a reset link has been sent.', 'info')
            logger.info(f'Password reset requested for: {email}')
        else:
            flash('If an account exists with that email, a reset link has been sent.', 'info')
    
    return render_template('auth/forgot_password.html')
