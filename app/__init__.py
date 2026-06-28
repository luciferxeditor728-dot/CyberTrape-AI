"""CyberTrap-AI Flask Application Package."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
from flask_caching import Cache
import logging
from logging.handlers import RotatingFileHandler
import os

from app.config import config_by_name

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
cache = Cache()


def create_app(config_name=None):
    """Application factory function."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    cache.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ALLOWED_ORIGINS', '*')}})
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register CLI commands
    register_cli_commands(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_blueprints(app):
    """Register Flask blueprints."""
    from app.routes import auth_bp, dashboard_bp, users_bp, profile_bp
    from app.routes import settings_bp, notifications_bp, admin_bp, analytics_bp
    from app.routes import api_auth_bp, api_users_bp, api_analytics_bp, api_admin_bp
    from app.routes.errors import errors_bp
    
    # Web routes
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(analytics_bp)
    
    # API routes
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(api_users_bp)
    app.register_blueprint(api_analytics_bp)
    app.register_blueprint(api_admin_bp)
    
    # Error routes
    app.register_blueprint(errors_bp)


def register_error_handlers(app):
    """Register error handlers."""
    from app.routes.errors import handle_400, handle_403, handle_404, handle_500
    
    app.register_error_handler(400, handle_400)
    app.register_error_handler(403, handle_403)
    app.register_error_handler(404, handle_404)
    app.register_error_handler(500, handle_500)


def register_cli_commands(app):
    """Register CLI commands."""
    @app.cli.command()
    def init_db():
        """Initialize the database."""
        db.create_all()
        print('Database initialized successfully!')
    
    @app.cli.command()
    def seed_db():
        """Seed the database with sample data."""
        from scripts.seed_data import seed
        seed()
        print('Database seeded successfully!')


def setup_logging(app):
    """Setup application logging."""
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/cybertrap.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('CyberTrap-AI startup')
