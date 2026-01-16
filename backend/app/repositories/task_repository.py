from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional
from uuid import UUID


class TaskRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_task(self, task_create: TaskCreate) -> Task:
        """Create a new task"""
        db_task = Task(**task_create.model_dump())
        self.db_session.add(db_task)
        await self.db_session.commit()
        await self.db_session.refresh(db_task)
        return db_task

    async def get_task_by_id(self, task_id: UUID) -> Optional[Task]:
        """Get a task by its ID"""
        stmt = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        stmt = select(Task).order_by(Task.created_at.desc())
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def update_task(self, task_id: UUID, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task"""
        # Get the task to update
        db_task = await self.get_task_by_id(task_id)
        if not db_task:
            return None

        # Prepare update data, excluding None values
        update_data = task_update.model_dump(exclude_unset=True)

        # Update the task
        stmt = update(Task).where(Task.id == task_id).values(**update_data)
        await self.db_session.execute(stmt)

        # Commit the transaction before refreshing
        await self.db_session.commit()

        # Refresh the task to get updated values
        await self.db_session.refresh(db_task)

        return db_task

    async def delete_task(self, task_id: UUID) -> bool:
        """Delete a task"""
        stmt = delete(Task).where(Task.id == task_id)
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount > 0