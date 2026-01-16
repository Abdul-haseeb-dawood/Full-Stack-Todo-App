from typing import List, Optional
from uuid import UUID
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    async def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """Create a new task"""
        db_task = await self.task_repository.create_task(task_create)
        return TaskResponse.model_validate(db_task)

    async def get_task_by_id(self, task_id: UUID) -> Optional[TaskResponse]:
        """Get a task by its ID"""
        db_task = await self.task_repository.get_task_by_id(task_id)
        if db_task:
            return TaskResponse.model_validate(db_task)
        return None

    async def get_all_tasks(self) -> List[TaskResponse]:
        """Get all tasks"""
        db_tasks = await self.task_repository.get_all_tasks()
        return [TaskResponse.model_validate(task) for task in db_tasks]

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Optional[TaskResponse]:
        """Update a task"""
        db_task = await self.task_repository.update_task(task_id, task_update)
        if db_task:
            return TaskResponse.model_validate(db_task)
        return None

    async def delete_task(self, task_id: UUID) -> bool:
        """Delete a task"""
        return await self.task_repository.delete_task(task_id)