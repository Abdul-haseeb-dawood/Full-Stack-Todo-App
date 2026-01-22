import sys
import os
# Add the backend directory to the Python path to import backend functions
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from app.schemas.task import TaskUpdate
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.db.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, Optional

async def update_task(task_id: str, title: Optional[str] = None, description: Optional[str] = None,
                      priority: Optional[str] = None, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Update a task in the todo app

    Args:
        task_id: The ID of the task to update
        title: The new title of the task (optional)
        description: The new description of the task (optional)
        priority: The new priority level of the task (optional)
        completed: The new completion status of the task (optional)

    Returns:
        A dictionary containing the updated task or an error message
    """
    try:
        # Use the existing database session from the app
        async with AsyncSession(bind=engine) as session:
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)

            # Prepare the update object with only the fields that are provided
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description
            if priority is not None:
                update_data["priority"] = priority
            if completed is not None:
                update_data["completed"] = completed

            task_update = TaskUpdate(**update_data)

            updated_task = await task_service.update_task(task_id, task_update)

            if updated_task:
                return {
                    "success": True,
                    "task": updated_task.dict(),
                    "message": f"Task with ID {task_id} updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found"
                }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }