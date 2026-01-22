from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository


class InputSchema(BaseModel):
    user_id: str
    task_id: str


name = "delete_task"
description = "Delete a task from the user's task list"


def get_input_schema():
    return {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "string", "description": "The ID of the task to delete"}
        },
        "required": ["user_id", "task_id"]
    }


async def execute(db_session: AsyncSession, user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Execute the delete_task tool by removing a task from the database
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
    
    # Delete the task from the database
    deleted = await task_service.delete_task(uuid_task_id)
    
    if deleted:
        return {
            "status": "success",
            "message": f"Task with ID {task_id} deleted successfully",
            "task_id": task_id
        }
    else:
        return {
            "status": "error",
            "message": f"Task with id {task_id} not found"
        }