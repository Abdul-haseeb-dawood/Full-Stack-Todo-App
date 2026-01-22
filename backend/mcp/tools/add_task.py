import sys
import os
# Add the backend directory to the Python path to import backend functions
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

from app.schemas.task import TaskCreate
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.db.database import engine  # Use the existing engine from the app
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Dict, Any

async def add_task(title: str, description: str = "", priority: str = "medium") -> Dict[str, Any]:
    """
    Add a new task to the todo app

    Args:
        title: The title of the task
        description: The description of the task (optional)
        priority: The priority level of the task (low, medium, high) (optional)

    Returns:
        A dictionary containing the created task or an error message
    """
    try:
        # Use the existing database session from the app
        async with AsyncSession(bind=engine) as session:
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)

            # Create the task
            task_create = TaskCreate(
                title=title,
                description=description,
                priority=priority
            )

            created_task = await task_service.create_task(task_create)

            return {
                "success": True,
                "task": created_task.dict(),
                "message": f"Task '{title}' added successfully"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import asyncio
    async def test_add_task():
        result = await add_task("Test task from command line")
        print("Result:", result)

    asyncio.run(test_add_task())