from pydantic import BaseModel
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.task_service import TaskService
from app.schemas.task import TaskCreate
from app.repositories.task_repository import TaskRepository


class InputSchema(BaseModel):
    user_id: str
    title: str
    description: str = ""


name = "add_task"
description = "Add a new task to the user's task list"


def get_input_schema():
    return {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "The ID of the user"},
            "title": {"type": "string", "description": "The title of the task"},
            "description": {"type": "string", "description": "The description of the task"}
        },
        "required": ["user_id", "title"]
    }


async def execute(db_session: AsyncSession, user_id: str, title: str, description: str = "") -> Dict[str, Any]:
    """
    Execute the add_task tool by creating a new task in the database
    """
    # Create task repository and service
    task_repo = TaskRepository(db_session)
    task_service = TaskService(task_repo)

    # Prepare the task data
    task_data = TaskCreate(
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
        priority="medium"
    )

    # Create the task in the database
    task = await task_service.create_task(task_data)

    return {
        "status": "success",
        "message": f"Task '{title}' added successfully",
        "task_id": str(task.id),
        "task_title": title
    }