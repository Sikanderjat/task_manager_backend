from app.workers.celery_worker import celery
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

@celery.task
def example_task():
    """Example Celery task that logs execution"""
    try:
        result = f"Task completed at {datetime.utcnow()}"
        logger.info(result)
        return result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise
