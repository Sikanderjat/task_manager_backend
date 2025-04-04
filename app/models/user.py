from app.utils.db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index
from sqlalchemy.dialects.postgresql import ARRAY

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        Index('idx_user_email', 'email'),
        # Removed the index on 'role'
        {'comment': 'User accounts with role-based access control'}
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    roles = db.Column(ARRAY(db.String(20)), default=['user'])  # ['admin', 'manager', 'user']
    permissions = db.Column(ARRAY(db.String(50)), default=[])  # ['create_task', 'edit_all_tasks', ...]
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    assigned_tasks = db.relationship("TaskManager", 
                                   foreign_keys="TaskManager.assigned_to",
                                   back_populates="assigned_user")
    created_tasks = db.relationship("TaskManager",
                                  foreign_keys="TaskManager.created_by",
                                  back_populates="creator")
    task_logs = db.relationship("TaskLogger",
                              foreign_keys="TaskLogger.changed_by",
                              back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role_name):
        """Check if user has specified role"""
        return role_name in self.roles

    def has_permission(self, permission_name):
        """Check if user has specified permission"""
        return permission_name in self.permissions

    def can(self, permission_name):
        """Convenience method combining role and permission checks"""
        return (self.has_permission(permission_name) or
                self.has_role('admin') or
                (self.has_role('manager') and 
                 permission_name in ['create_task', 'edit_task']))

    def __repr__(self):
        return f"<User {self.username} ({', '.join(self.roles)})>"
