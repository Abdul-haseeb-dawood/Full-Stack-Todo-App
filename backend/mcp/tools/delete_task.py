import sys
import os
# Add the backend directory to the Python path to import backend functions
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.db.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

async def delete_task(task_id: str) -> Dict[str, Any]:
    """
    Delete a task from the todo app

    Args:
        task_id: The ID of the task to delete

    Returns:
        A dictionary containing success status or an error message
    """
    try:
        # Use the existing database session from the app
        async with AsyncSession(bind=engine) as session:
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)

            deleted = await task_service.delete_task(task_id)

            if deleted:
                return {
                    "success": True,
                    "message": f"Task with ID {task_id} deleted successfully"
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