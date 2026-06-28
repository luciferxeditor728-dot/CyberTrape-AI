"""Email tasks."""
from app.tasks.celery import make_celery
from flask import current_app
from app.utils.logger import get_logger

logger = get_logger(__name__)


# Initialize Celery
celery = None


def init_celery(app):
    """Initialize Celery with Flask app."""
    global celery
    celery = make_celery(app)
    return celery


@celery.task(bind=True, max_retries=3)
def send_email(self, email, subject, body, html_body=None):
    """Send email task."""
    try:
        from app import mail
        from flask_mail import Message
        
        msg = Message(
            subject=subject,
            recipients=[email],
            body=body,
            html=html_body
        )
        mail.send(msg)
        logger.info(f'Email sent to {email}')
        return {'status': 'success', 'email': email}
    except Exception as exc:
        logger.error(f'Failed to send email to {email}: {str(exc)}')
        raise self.retry(exc=exc, countdown=60)


@celery.task
def cleanup_sessions():
    """Cleanup expired sessions."""
    from app.models import Session
    from app import db
    from datetime import datetime
    
    expired = Session.query.filter(Session.expires_at < datetime.utcnow()).delete()
    db.session.commit()
    logger.info(f'Deleted {expired} expired sessions')
    return {'status': 'success', 'deleted': expired}


@celery.task
def cleanup_notifications():
    """Cleanup old notifications."""
    from app.models import Notification
    from app import db
    from datetime import datetime
    
    deleted = Notification.query.filter(Notification.expires_at < datetime.utcnow()).delete()
    db.session.commit()
    logger.info(f'Deleted {deleted} expired notifications')
    return {'status': 'success', 'deleted': deleted}
