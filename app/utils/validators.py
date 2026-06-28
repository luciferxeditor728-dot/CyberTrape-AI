"""Validators for input validation."""
import re
from datetime import datetime


class ValidationError(Exception):
    """Custom validation error."""
    pass


def validate_email(email):
    """Validate email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Invalid email format')
    return True


def validate_username(username):
    """Validate username."""
    if len(username) < 3:
        raise ValidationError('Username must be at least 3 characters')
    if len(username) > 80:
        raise ValidationError('Username must not exceed 80 characters')
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        raise ValidationError('Username can only contain alphanumeric characters, underscores, and hyphens')
    return True


def validate_password(password, config):
    """Validate password against policy."""
    if len(password) < config.get('PASSWORD_MIN_LENGTH', 8):
        raise ValidationError(f"Password must be at least {config.get('PASSWORD_MIN_LENGTH', 8)} characters")
    
    if config.get('PASSWORD_REQUIRE_UPPERCASE', False) and not re.search(r'[A-Z]', password):
        raise ValidationError('Password must contain at least one uppercase letter')
    
    if config.get('PASSWORD_REQUIRE_NUMBERS', False) and not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number')
    
    if config.get('PASSWORD_REQUIRE_SPECIAL', False) and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError('Password must contain at least one special character')
    
    return True


def validate_phone(phone):
    """Validate phone number."""
    phone = re.sub(r'\D', '', phone)
    if len(phone) < 10:
        raise ValidationError('Phone number must contain at least 10 digits')
    return True


def validate_url(url):
    """Validate URL."""
    pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)$'
    if not re.match(pattern, url):
        raise ValidationError('Invalid URL format')
    return True


def validate_ip_address(ip):
    """Validate IP address (IPv4 or IPv6)."""
    ipv4_pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    ipv6_pattern = r'^(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4})$'
    
    if not re.match(ipv4_pattern, ip) and not re.match(ipv6_pattern, ip):
        raise ValidationError('Invalid IP address')
    return True


def validate_date(date_string, format='%Y-%m-%d'):
    """Validate date string."""
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        raise ValidationError(f'Invalid date format. Expected {format}')


def validate_json(data, required_fields):
    """Validate JSON data has required fields."""
    for field in required_fields:
        if field not in data or data[field] is None:
            raise ValidationError(f'Missing required field: {field}')
    return True
