from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.schemas.task import TaskUpdate
from app.repositories.task_repository import TaskRepository


class InputSchema(BaseModel):
    user_id: str
    task_id: str


name = "complete_task"
description = "Mark a task as completed in the user's task list"


def get_input_schema():
    return {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "string", "description": "The ID of the task to mark as completed"}
        },
        "required": ["user_id", "task_id"]
    }


async def execute(db_session: AsyncSession, user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Execute the complete_task tool by marking a task as completed in the database
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
    
    # Prepare update data to mark as completed
    task_update = TaskUpdate(completed=True)
    
    # Update the task in the database
    updated_task = await task_service.update_task(uuid_task_id, task_update)
    
    if updated_task:
        return {
            "status": "success",
            "message": f"Task '{updated_task.title}' marked as completed",
            "task_id": str(updated_task.id),
            "task_title": updated_task.title
        }
    else:
        return {
            "status": "error",
            "message": f"Task with id {task_id} not found"
        }