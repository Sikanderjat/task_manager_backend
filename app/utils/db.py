from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool
from tenacity import retry, stop_after_attempt, wait_exponential
import os
import logging

logger = logging.getLogger(__name__)

class RetrySQLAlchemy(SQLAlchemy):
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def apply_driver_hacks(self, app, info, options):
        try:
            super().apply_driver_hacks(app, info, options)
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise

db = RetrySQLAlchemy(
    engine_options={
        'poolclass': QueuePool,
        'pool_size': 10,
        'max_overflow': 20,
        'pool_timeout': 30,
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }
)

def init_db(app):
    """Initialize database with retry mechanism"""
    db.init_app(app)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise
