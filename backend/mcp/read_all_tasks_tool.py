from pydantic import BaseModel
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository


class InputSchema(BaseModel):
    user_id: str
    status: str = "all"  # "all", "pending", "completed"
    priority: str = None


name = "read_all_tasks"
description = "Read all tasks from the user's task list"


def get_input_schema():
    return {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "The ID of the user"},
            "status": {"type": "string", "description": "Filter by status: 'all', 'pending', or 'completed'"},
            "priority": {"type": "string", "description": "Filter by priority"}
        },
        "required": ["user_id"]
    }


async def execute(db_session: AsyncSession, user_id: str, status: str = "all", priority: str = None) -> Dict[str, Any]:
    """
    Execute the read_all_tasks tool by fetching all tasks from the database
    """
    # Create task repository and service
    task_repo = TaskRepository(db_session)
    task_service = TaskService(task_repo)
    
    # Prepare filters
    filters = {"user_id": user_id}
    
    if status != "all":
        if status == "pending":
            filters["completed"] = False
        elif status == "completed":
            filters["completed"] = True

    if priority:
        filters["priority"] = priority

    # Get tasks from the database
    tasks = await task_service.get_tasks_by_filters(filters)
    
    task_list = [
        {
            "id": str(task.id),
            "user_id": task.user_id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "priority": task.priority,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        for task in tasks
    ]
    
    return {
        "status": "success",
        "tasks_count": len(task_list),
        "tasks": task_list
    }