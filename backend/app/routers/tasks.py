from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.database import get_async_session
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.utils.exceptions import TaskNotFoundException

router = APIRouter()


def get_task_service(db_session: AsyncSession = Depends(get_async_session)):
    """Dependency to get the task service with repository"""
    task_repo = TaskRepository(db_session)
    return TaskService(task_repo)


@router.post("/tasks", response_model=TaskResponse, status_code=201)
async def create_task(
    task_create: TaskCreate,
    task_service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    try:
        return await task_service.create_task(task_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=List[TaskResponse])
async def get_all_tasks(
    task_service: TaskService = Depends(get_task_service)
):
    """Get all tasks"""
    try:
        return await task_service.get_all_tasks()
    except Exception as e:
        # Log the actual error for debugging
        print(f"Database error in get_all_tasks: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    """Get a specific task by ID"""
    try:
        task = await task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        return task
    except ValueError:
        # Raised when task_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        # Check if this is a database connection error
        error_str = str(e)
        if "connection" in error_str.lower() or "database" in error_str.lower() or "sqlalchemy" in error_str.lower():
            print(f"Database error in get_task_by_id: {error_str}")
            raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")


@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """Update a specific task by ID"""
    try:
        task = await task_service.update_task(task_id, task_update)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        return task
    except ValueError:
        # Raised when task_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        # Check if this is a database connection error
        error_str = str(e)
        if "connection" in error_str.lower() or "database" in error_str.lower() or "sqlalchemy" in error_str.lower():
            print(f"Database error in update_task: {error_str}")
            raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    """Toggle the completion status of a task"""
    try:
        task = await task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")

        # Update the completion status
        updated_task = await task_service.update_task(task_id, TaskUpdate(completed=not task.completed))
        return updated_task
    except ValueError:
        # Raised when task_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        # Check if this is a database connection error
        error_str = str(e)
        if "connection" in error_str.lower() or "database" in error_str.lower() or "sqlalchemy" in error_str.lower():
            print(f"Database error in toggle_task_completion: {error_str}")
            raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail=f"Error toggling task completion: {str(e)}")


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: UUID,
    task_service: TaskService = Depends(get_task_service)
):
    """Delete a specific task by ID"""
    try:
        deleted = await task_service.delete_task(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        return
    except ValueError:
        # Raised when task_id is not a valid UUID
        raise HTTPException(status_code=400, detail="Invalid task ID format")
    except Exception as e:
        # Check if this is a database connection error
        error_str = str(e)
        if "connection" in error_str.lower() or "database" in error_str.lower() or "sqlalchemy" in error_str.lower():
            print(f"Database error in delete_task: {error_str}")
            raise HTTPException(status_code=503, detail="Service temporarily unavailable. Please try again later.")
        else:
            raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")