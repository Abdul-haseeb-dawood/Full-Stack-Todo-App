from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate, TaskUpdate
import uuid


class MCPTaskTools:
    def __init__(self, db_session: AsyncSession):
        from app.repositories.task_repository import TaskRepository
        task_repo = TaskRepository(db_session)
        self.task_service = TaskService(task_repo)

    async def add_task(self, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Create a new task"""
        task_data = TaskCreate(
            user_id=user_id,
            title=title,
            description=description or "",
            completed=False
        )
        task = await self.task_service.create_task(task_data)

        return {
            "task_id": str(task.id),
            "status": "created",
            "title": task.title
        }

    async def read_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Read a specific task by ID"""
        # Convert task_id to UUID
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task ID format: {task_id}. Expected UUID.")

        # Get the task by ID
        task = await self.task_service.get_task_by_id(uuid_task_id)

        if task and task.user_id == user_id:
            return {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority
            }
        else:
            raise ValueError(f"Task with id {task_id} not found or does not belong to user {user_id}")

    async def read_all_tasks(self, user_id: str, status: str = "all", priority: str = None) -> List[Dict[str, Any]]:
        """Read all tasks with optional filters"""
        filters = {"user_id": user_id}

        if status != "all":
            if status == "pending":
                filters["completed"] = False
            elif status == "completed":
                filters["completed"] = True

        if priority:
            filters["priority"] = priority

        tasks = await self.task_service.get_tasks_by_filters(filters)

        return [
            {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority
            }
            for task in tasks
        ]

    # Alias for backward compatibility with existing tools
    async def list_tasks(self, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
        """Alias for read_all_tasks to maintain compatibility"""
        return await self.read_all_tasks(user_id, status)

    async def update_task(self, user_id: str, task_id: str, title: str = None, description: str = None,
                         completed: bool = None, priority: str = None) -> Dict[str, Any]:
        """Update task fields"""
        # Convert task_id to UUID
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task ID format: {task_id}. Expected UUID.")

        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if completed is not None:
            update_data["completed"] = completed
        if priority is not None:
            update_data["priority"] = priority

        task_update = TaskUpdate(**update_data)
        updated_task = await self.task_service.update_task(uuid_task_id, task_update)

        if updated_task:
            return {
                "task_id": str(updated_task.id),
                "status": "updated",
                "title": updated_task.title
            }
        else:
            raise ValueError(f"Task with id {task_id} not found")

    async def complete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Mark a task as complete"""
        # Convert task_id to UUID
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task ID format: {task_id}. Expected UUID.")

        task_update = TaskUpdate(completed=True)
        updated_task = await self.task_service.update_task(uuid_task_id, task_update)

        if updated_task:
            return {
                "task_id": str(updated_task.id),
                "status": "completed",
                "title": updated_task.title
            }
        else:
            raise ValueError(f"Task with id {task_id} not found")

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """Remove a task from the list"""
        # Convert task_id to UUID
        try:
            uuid_task_id = uuid.UUID(task_id)
        except ValueError:
            raise ValueError(f"Invalid task ID format: {task_id}. Expected UUID.")

        deleted = await self.task_service.delete_task(uuid_task_id)

        if deleted:
            return {
                "task_id": str(uuid_task_id),
                "status": "deleted"
            }
        else:
            raise ValueError(f"Task with id {task_id} not found")