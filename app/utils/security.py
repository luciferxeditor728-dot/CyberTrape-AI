"""Security utilities."""
import hashlib
import hmac
from flask import current_app
import secrets
from datetime import datetime, timedelta
import jwt


def hash_password(password):
    """Hash password using bcrypt."""
    from werkzeug.security import generate_password_hash
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """Verify password against hash."""
    from werkzeug.security import check_password_hash
    return check_password_hash(password_hash, password)


def generate_jwt_token(user_id, expires_in=None):
    """Generate JWT token for user."""
    if expires_in is None:
        expires_in = current_app.config.get('JWT_EXPIRATION', 3600)
    
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow(),
    }
    
    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )
    
    return token


def verify_jwt_token(token):
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(
            token,
            current_app.config['JWT_SECRET_KEY'],
            algorithms=[current_app.config['JWT_ALGORITHM']]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def generate_totp_secret():
    """Generate TOTP secret for 2FA."""
    import pyotp
    return pyotp.random_base32()


def verify_totp(secret, token):
    """Verify TOTP token."""
    import pyotp
    totp = pyotp.TOTP(secret)
    return totp.verify(token)


def generate_backup_codes(count=10):
    """Generate backup codes for 2FA."""
    codes = []
    for _ in range(count):
        code = secrets.token_hex(4).upper()
        codes.append(code)
    return codes


def verify_backup_code(code, codes_hash):
    """Verify backup code."""
    code_hash = hashlib.sha256(code.encode()).hexdigest()
    return code_hash in codes_hash


def hash_backup_codes(codes):
    """Hash backup codes for storage."""
    return [hashlib.sha256(code.encode()).hexdigest() for code in codes]


def generate_csrf_token():
    """Generate CSRF token."""
    return secrets.token_urlsafe(32)


def verify_csrf_token(token, session_token):
    """Verify CSRF token."""
    return hmac.compare_digest(token, session_token)


def hash_api_key(key):
    """Hash API key for storage."""
    return hashlib.sha256(key.encode()).hexdigest()


def encrypt_sensitive_data(data, key=None):
    """Encrypt sensitive data."""
    from cryptography.fernet import Fernet
    if key is None:
        key = current_app.config['SECRET_KEY'].encode()
    
    cipher = Fernet(key)
    encrypted = cipher.encrypt(data.encode())
    return encrypted.decode()


def decrypt_sensitive_data(encrypted_data, key=None):
    """Decrypt sensitive data."""
    from cryptography.fernet import Fernet
    if key is None:
        key = current_app.config['SECRET_KEY'].encode()
    
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_data.encode())
    return decrypted.decode()
