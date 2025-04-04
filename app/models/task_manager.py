from app.utils.db import db
from datetime import datetime
from sqlalchemy import Index
from sqlalchemy.event import listens_for
from app.models.task_logger import TaskLogger

class TaskManager(db.Model):
    __tablename__ = "tasks"
    __table_args__ = (
        Index('idx_task_status', 'status'),
        Index('idx_task_assigned', 'assigned_to'),
        {'comment': 'Stores active tasks for management'}
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default="pending", 
                      comment="pending, in_progress, completed, archived")
    priority = db.Column(db.Integer, default=3, comment="1=high, 2=medium, 3=low")
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True, comment="Soft delete flag")

    assigned_user = db.relationship("User", foreign_keys=[assigned_to], backref="assigned_tasks_list")  # Changed backref name
    creator = db.relationship("User", foreign_keys=[created_by], backref="created_tasks")
    logs = db.relationship("TaskLogger", backref="task", lazy="dynamic", 
                         cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Task {self.title}>"

    def can_edit(self, user):
        """Check if user has permission to edit this task"""
        return (user.id == self.created_by or 
                user.id == self.assigned_to or
                user.has_role('admin'))

@listens_for(TaskManager, 'after_update')
def log_task_changes(mapper, connection, target):
    """Automatically log changes to task status"""
    if db.session.is_modified(target, include_collections=False):
        changes = {col.name: getattr(target, col.name) 
                  for col in target.__table__.columns 
                  if db.session.is_modified(target, col.name)}
        
        if changes:
            log = TaskLogger(
                task_id=target.id,
                changed_by=target.updated_by if hasattr(target, 'updated_by') else None,
                changes=changes,
                change_type="update"
            )
            db.session.add(log)
