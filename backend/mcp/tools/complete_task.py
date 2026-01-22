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
from typing import Dict, Any

async def complete_task(task_id: str) -> Dict[str, Any]:
    """
    Toggle the completion status of a task in the todo app

    Args:
        task_id: The ID of the task to toggle completion status

    Returns:
        A dictionary containing the updated task or an error message
    """
    try:
        # Use the existing database session from the app
        async with AsyncSession(bind=engine) as session:
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)

            # First, get the current task to check its completion status
            current_task = await task_service.get_task_by_id(task_id)
            if not current_task:
                return {
                    "success": False,
                    "error": f"Task with ID {task_id} not found"
                }

            # Toggle the completion status
            new_completed_status = not current_task.completed

            # Update the task with the new completion status
            task_update = TaskUpdate(completed=new_completed_status)
            updated_task = await task_service.update_task(task_id, task_update)

            if updated_task:
                return {
                    "success": True,
                    "task": updated_task.dict(),
                    "message": f"Task with ID {task_id} completion status toggled successfully"
                }
            else:
                return {
                    "success": False,
                    "error": f"Failed to update task with ID {task_id}"
                }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }