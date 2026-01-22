import sys
import os
# Add the backend directory to the Python path to import backend functions
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.db.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncio
from typing import Dict, Any, List

async def read_tasks() -> Dict[str, Any]:
    """
    Read all tasks from the todo app

    Returns:
        A dictionary containing all tasks or an error message
    """
    try:
        # Use the existing database session from the app
        async with AsyncSession(bind=engine) as session:
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)

            tasks = await task_service.get_all_tasks()

            # Convert tasks to dictionaries
            task_dicts = [task.dict() for task in tasks]

            return {
                "success": True,
                "tasks": task_dicts,
                "count": len(task_dicts),
                "message": f"Retrieved {len(task_dicts)} tasks successfully"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


async def read_task_by_id(task_id: str) -> Dict[str, Any]:
    """
    Read a specific task by its ID

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        A dictionary containing the task or an error message
    """
    try:
        # Use the existing database session from the app
        async with AsyncSession(bind=engine) as session:
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)

            task = await task_service.get_task_by_id(task_id)

            if task:
                return {
                    "success": True,
                    "task": task.dict(),
                    "message": f"Retrieved task with ID {task_id} successfully"
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

if __name__ == "__main__":
    async def test_read_tasks():
        result = await read_tasks()
        print("Result:", result)

    asyncio.run(test_read_tasks())