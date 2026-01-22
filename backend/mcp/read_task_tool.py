from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository


class InputSchema(BaseModel):
    user_id: str
    task_id: str


name = "read_task"
description = "Read a specific task from the user's task list"


def get_input_schema():
    return {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "string", "description": "The ID of the task to read"}
        },
        "required": ["user_id", "task_id"]
    }


async def execute(db_session: AsyncSession, user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Execute the read_task tool by fetching a task from the database
    """
    import uuid
    
    # Validate task_id format
    try:
        uuid_task_id = uuid.UUID(task_id)
    except ValueError:
        return {
            "status": "error",
            "message": f"Invalid task ID format: {task_id}. Expected UUID."
        }
    
    # Create task repository and service
    task_repo = TaskRepository(db_session)
    task_service = TaskService(task_repo)
    
    # Get the task from the database
    task = await task_service.get_task_by_id(uuid_task_id)
    
    if task and task.user_id == user_id:
        return {
            "status": "success",
            "task": {
                "id": str(task.id),
                "user_id": task.user_id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }
    else:
        return {
            "status": "error",
            "message": f"Task with id {task_id} not found or does not belong to user {user_id}"
        }