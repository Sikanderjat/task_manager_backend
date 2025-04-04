from datetime import datetime
from typing import List, Optional
from app.models.task_manager import Task
from app.repositories.task_repository import TaskRepository
from app.utils.redis_cache import cache

class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    @cache(ttl=60)
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        return self.task_repository.get_by_id(task_id)

    def get_all_tasks(self) -> List[Task]:
        return self.task_repository.get_all()

    def create_task(self, title: str, description: str, due_date: datetime) -> Task:
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            status='pending'
        )
        return self.task_repository.create(task)

    def update_task_status(self, task_id: int, status: str) -> Optional[Task]:
        task = self.task_repository.get_by_id(task_id)
        if task:
            task.status = status
            return self.task_repository.update(task)
        return None

    def delete_task(self, task_id: int) -> bool:
        task = self.task_repository.get_by_id(task_id)
        if task:
            self.task_repository.delete(task)
            return True
        return False
