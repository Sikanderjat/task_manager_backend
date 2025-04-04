from app.services.celery_worker import celery
from app.models.task_manager import TaskManager
from app.models.user import User
from app.utils.db import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@celery.task(bind=True, name='load_daily_tasks')
def load_daily_tasks(self):
    """Celery task to load and manage daily recurring tasks"""
    try:
        # Get all active users who should receive daily tasks
        users = User.query.filter_by(is_active=True).all()
        
        for user in users:
            # Check if user already has pending tasks
            pending_tasks = TaskManager.query.filter_by(
                assigned_to=user.id,
                status='pending'
            ).count()

            if pending_tasks >= 5:  # Max pending tasks per user
                continue

            # Create new daily task
            new_task = TaskManager(
                title=f"Daily Check-in {datetime.utcnow().strftime('%Y-%m-%d')}",
                description="Complete your daily check-in and task review",
                status="pending",
                priority=3,  # Low priority
                assigned_to=user.id,
                created_by=1  # System user
            )

            db.session.add(new_task)
            db.session.commit()

            # Log the task creation
            self.create_task_log(
                task_id=new_task.id,
                changed_by=1,  # System user
                change_type="create",
                changes={"status": "pending"}
            )

            logger.info(f"Created daily task for user {user.id}")

        return {"status": "success", "tasks_created": len(users)}
    
    except Exception as e:
        logger.error(f"Failed to load daily tasks: {str(e)}")
        return {"status": "error", "message": str(e)}
