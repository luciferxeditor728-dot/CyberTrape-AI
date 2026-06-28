"""Flask application configuration."""
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration for all environments."""
    
    # Core
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://user:password@localhost:5432/cybertrap_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Session
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # JWT
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
    JWT_EXPIRATION = int(os.getenv('JWT_EXPIRATION', 3600))
    REFRESH_TOKEN_EXPIRATION = int(os.getenv('REFRESH_TOKEN_EXPIRATION', 2592000))
    
    # Redis & Caching
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/1')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
    
    # Email
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@cybertrap.ai')
    
    # Security
    2FA_ENABLED = os.getenv('2FA_ENABLED', 'True') == 'True'
    TOTP_ISSUER = os.getenv('TOTP_ISSUER', 'CyberTrap-AI')
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_SPECIAL = True
    PASSWORD_REQUIRE_NUMBERS = True
    PASSWORD_REQUIRE_UPPERCASE = True
    
    # API
    API_RATE_LIMIT = int(os.getenv('API_RATE_LIMIT', 100))
    API_RATE_LIMIT_PERIOD = int(os.getenv('API_RATE_LIMIT_PERIOD', 3600))
    
    # CORS
    CORS_ALLOWED_ORIGINS = os.getenv(
        'CORS_ALLOWED_ORIGINS',
        'http://localhost:3000,http://localhost:5000'
    ).split(',')
    
    # Pagination
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))
    
    # Honeypot Configuration
    HONEYPOT_SSH_PORT = int(os.getenv('HONEYPOT_SSH_PORT', 2222))
    HONEYPOT_HTTP_PORT = int(os.getenv('HONEYPOT_HTTP_PORT', 8080))
    HONEYPOT_FTP_PORT = int(os.getenv('HONEYPOT_FTP_PORT', 2121))
    HONEYPOT_TELNET_PORT = int(os.getenv('HONEYPOT_TELNET_PORT', 2323))
    HONEYPOT_LOG_PATH = os.getenv('HONEYPOT_LOG_PATH', '/var/log/honeypot/')
    HONEYPOT_DATA_PATH = os.getenv('HONEYPOT_DATA_PATH', '/data/honeypot/')
    
    # AWS (Optional)
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    S3_BUCKET = os.getenv('S3_BUCKET', '')
    
    # Features
    FEATURE_ANALYTICS = os.getenv('FEATURE_ANALYTICS', 'True') == 'True'
    FEATURE_NOTIFICATIONS = os.getenv('FEATURE_NOTIFICATIONS', 'True') == 'True'
    FEATURE_BACKUP = os.getenv('FEATURE_BACKUP', 'True') == 'True'
    FEATURE_AUDIT_LOG = os.getenv('FEATURE_AUDIT_LOG', 'True') == 'True'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_ECHO = True


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_ECHO = False


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
}
