"""Logger setup."""
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import current_app


def get_logger(name):
    """Get or create logger."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # Create logs directory if not exists
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Setup file handler
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10485760,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        logger.addHandler(file_handler)
        
        # Setup console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s'
        ))
        logger.addHandler(console_handler)
        
        logger.setLevel(logging.INFO)
    
    return logger
