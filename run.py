"""Application entry point."""
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User, Role, Permission, Admin, ActivityLog, AuditLog, Notification, Session, Backup, APIKey

# Load environment variables
load_dotenv()

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Initialize Celery
from app.tasks.email_tasks import init_celery
celery = init_celery(app)


@app.shell_context_processor
def make_shell_context():
    """Create shell context for flask shell."""
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Permission': Permission,
        'Admin': Admin,
        'ActivityLog': ActivityLog,
        'AuditLog': AuditLog,
        'Notification': Notification,
        'Session': Session,
        'Backup': Backup,
        'APIKey': APIKey,
    }


@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized!')


@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    from datetime import datetime
    
    # Create default roles
    admin_role = Role(
        name='admin',
        description='Administrator role',
        is_system_role=True,
        is_active=True
    )
    analyst_role = Role(
        name='analyst',
        description='Security Analyst role',
        is_system_role=True,
        is_active=True
    )
    operator_role = Role(
        name='operator',
        description='Operator role',
        is_system_role=True,
        is_active=True
    )
    viewer_role = Role(
        name='viewer',
        description='Viewer role',
        is_system_role=True,
        is_active=True
    )
    
    db.session.add_all([admin_role, analyst_role, operator_role, viewer_role])
    db.session.commit()
    
    # Create default permissions
    permissions_data = [
        ('user_create', 'Create users', 'user'),
        ('user_read', 'Read users', 'user'),
        ('user_update', 'Update users', 'user'),
        ('user_delete', 'Delete users', 'user'),
        ('admin_access', 'Admin access', 'admin'),
    ]
    
    for name, desc, category in permissions_data:
        perm = Permission(
            name=name,
            description=desc,
            category=category,
            is_system_permission=True,
            is_active=True
        )
        db.session.add(perm)
    
    db.session.commit()
    
    # Create admin user
    admin_user = User(
        username='admin',
        email='admin@cybertrap.ai',
        first_name='Admin',
        last_name='User',
        is_active=True,
        is_verified=True,
        role=admin_role
    )
    admin_user.set_password('Admin@123456')
    
    db.session.add(admin_user)
    db.session.commit()
    
    print('Database seeded with default data!')
    print('Admin user created: admin / Admin@123456')


@app.cli.command()
def create_admin():
    """Create a new admin user."""
    import click
    
    username = click.prompt('Username')
    email = click.prompt('Email')
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    
    if User.query.filter_by(username=username).first():
        print('User already exists!')
        return
    
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        print('Admin role not found. Please seed database first.')
        return
    
    user = User(
        username=username,
        email=email,
        is_active=True,
        is_verified=True,
        role=admin_role
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    print(f'Admin user {username} created successfully!')


if __name__ == '__main__':
    app.run()
