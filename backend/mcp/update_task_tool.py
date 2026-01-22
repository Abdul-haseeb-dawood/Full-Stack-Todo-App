from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.schemas.task import TaskUpdate
from app.repositories.task_repository import TaskRepository


class InputSchema(BaseModel):
    user_id: str
    task_id: str
    title: str = None
    description: str = None
    completed: bool = None
    priority: str = None


name = "update_task"
description = "Update an existing task in the user's task list"


def get_input_schema():
    return {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "The ID of the user"},
            "task_id": {"type": "string", "description": "The ID of the task to update"},
            "title": {"type": "string", "description": "The new title of the task"},
            "description": {"type": "string", "description": "The new description of the task"},
            "completed": {"type": "boolean", "description": "Whether the task is completed"},
            "priority": {"type": "string", "description": "The new priority of the task"}
        },
        "required": ["user_id", "task_id"]
    }


async def execute(db_session: AsyncSession, user_id: str, task_id: str, title: str = None, description: str = None, completed: bool = None, priority: str = None) -> Dict[str, Any]:
    """
    Execute the update_task tool by updating a task in the database
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
    
    # Prepare update data
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
    
    # Update the task in the database
    updated_task = await task_service.update_task(uuid_task_id, task_update)
    
    if updated_task:
        return {
            "status": "success",
            "message": f"Task '{updated_task.title}' updated successfully",
            "task_id": str(updated_task.id),
            "task_title": updated_task.title
        }
    else:
        return {
            "status": "error",
            "message": f"Task with id {task_id} not found"
        }