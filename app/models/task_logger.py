from app.utils.db import db
from datetime import datetime
import json
from sqlalchemy import Index

class TaskLogger(db.Model):
    __tablename__ = "task_logs"
    __table_args__ = (
        Index('idx_log_task', 'task_id'),
        Index('idx_log_timestamp', 'timestamp'),
        {'comment': 'Audit log for task changes'}
    )

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    change_type = db.Column(db.String(20), nullable=False)  # create, update, delete, status_change
    changes = db.Column(db.JSON, comment="JSON of changed fields and values")
    comment = db.Column(db.Text, nullable=True)

    task = db.relationship("TaskManager", back_populates="logs")
    user = db.relationship("User", backref="logs")  # Changed backref name from 'task_logs' to 'logs'

    def __repr__(self):
        return f"<TaskLog {self.change_type} by User {self.changed_by}>"

    @classmethod
    def create_from_changes(cls, task_id, changed_by, change_type, changes, comment=None):
        """Helper method to create a new log entry"""
        return cls(
            task_id=task_id,
            changed_by=changed_by,
            change_type=change_type,
            changes=json.dumps(changes) if changes else None,
            comment=comment
        )
