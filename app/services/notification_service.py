"""Notification service."""
from app import db, mail
from app.models import Notification
from flask_mail import Message
from app.utils.logger import get_logger
from datetime import datetime, timedelta

logger = get_logger(__name__)


class NotificationService:
    """Notification management service."""
    
    @staticmethod
    def create_notification(user_id, title, message, notification_type='info', channels=None, entity_type=None, entity_id=None):
        """Create notification for user."""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            channels=channels or ['dashboard'],
            related_entity_type=entity_type,
            related_entity_id=entity_id,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        
        db.session.add(notification)
        db.session.commit()
        
        logger.info(f'Notification created for user: {user_id}')
        return notification
    
    @staticmethod
    def get_user_notifications(user_id, unread_only=False):
        """Get user notifications."""
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        return query.order_by(Notification.created_at.desc()).all()
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark notification as read."""
        notification = Notification.query.get(notification_id)
        
        if notification:
            notification.mark_as_read()
            db.session.commit()
            logger.info(f'Notification marked as read: {notification_id}')
        
        return notification
    
    @staticmethod
    def send_email_notification(email, subject, body, html_body=None):
        """Send email notification."""
        try:
            msg = Message(
                subject=subject,
                recipients=[email],
                body=body,
                html=html_body
            )
            mail.send(msg)
            logger.info(f'Email sent to: {email}')
            return True
        except Exception as e:
            logger.error(f'Failed to send email to {email}: {str(e)}')
            return False
    
    @staticmethod
    def delete_old_notifications(days=30):
        """Delete expired notifications."""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        deleted = Notification.query.filter(
            Notification.created_at < cutoff_date
        ).delete()
        
        db.session.commit()
        logger.info(f'Deleted {deleted} old notifications')
        return deleted
