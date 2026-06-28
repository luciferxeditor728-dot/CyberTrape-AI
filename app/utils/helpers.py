"""Helper functions."""
from flask import request
import json
from datetime import datetime
import secrets
import string


def get_client_ip():
    """Get client IP address from request."""
    if request.environ.get('HTTP_CF_CONNECTING_IP'):
        return request.environ.get('HTTP_CF_CONNECTING_IP')
    elif request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    return request.remote_addr


def get_user_agent():
    """Get user agent from request."""
    return request.headers.get('User-Agent', 'Unknown')


def get_request_info():
    """Get request information."""
    return {
        'ip_address': get_client_ip(),
        'user_agent': get_user_agent(),
        'endpoint': request.endpoint,
        'method': request.method,
        'path': request.path,
    }


def generate_token(length=32):
    """Generate a random token."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


def generate_password(length=16):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(secrets.choice(characters) for _ in range(length))


def paginate(query, page, per_page):
    """Paginate query results."""
    return query.paginate(page=page, per_page=per_page, error_out=False)


def serialize_datetime(dt):
    """Serialize datetime to ISO format string."""
    if dt is None:
        return None
    return dt.isoformat()


def parse_datetime(dt_string):
    """Parse ISO format datetime string."""
    return datetime.fromisoformat(dt_string)


def dict_to_json(data):
    """Convert dict to JSON string."""
    return json.dumps(data)


def json_to_dict(json_string):
    """Convert JSON string to dict."""
    return json.loads(json_string)


def truncate_string(s, length=100):
    """Truncate string to specified length."""
    if len(s) > length:
        return s[:length] + '...'
    return s


def format_bytes(bytes_size):
    """Format bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"


def get_time_ago(dt):
    """Get human readable time difference."""
    diff = datetime.utcnow() - dt
    
    if diff.days > 0:
        return f"{diff.days} day(s) ago"
    elif diff.seconds > 3600:
        return f"{diff.seconds // 3600} hour(s) ago"
    elif diff.seconds > 60:
        return f"{diff.seconds // 60} minute(s) ago"
    else:
        return "just now"
