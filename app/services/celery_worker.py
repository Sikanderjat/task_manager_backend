from celery import Celery
from app.config import Config
from app.utils.db import db
from app.models.task_manager import TaskManager
from app.models.task_logger import TaskLogger
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=Config.REDIS_URL,
        backend=Config.REDIS_URL,
        include=['app.services.daily_task_loader']
    )
    
    celery.conf.update(app.config)
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_default_queue='default',
        task_routes={
            'app.services.daily_task_loader.*': {'queue': 'periodic'}
        }
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

def create_task_log(task_id, changed_by, change_type, changes=None):
    """Helper function to create task log entries"""
    try:
        log = TaskLogger.create_from_changes(
            task_id=task_id,
            changed_by=changed_by,
            change_type=change_type,
            changes=changes
        )
        db.session.add(log)
        db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Failed to create task log: {str(e)}")
        db.session.rollback()
        return False
