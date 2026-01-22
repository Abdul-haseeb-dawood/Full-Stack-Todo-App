import asyncio
from app.db.database import AsyncSessionLocal
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate


async def test_database():
    """Test if database operations work correctly"""
    async with AsyncSessionLocal() as db_session:
        # Create task service
        task_repo = TaskRepository(db_session)
        task_service = TaskService(task_repo)

        # Try to create a test task
        task_data = TaskCreate(
            user_id="test_user_123",
            title="Test task from database test",
            description="This is a test task to verify database connectivity",
            completed=False
        )

        try:
            created_task = await task_service.create_task(task_data)
            print(f"Task created successfully: {created_task.title}")
            print(f"Task ID: {created_task.id}")
            print(f"User ID: {created_task.user_id}")

            # Try to retrieve the task
            all_tasks = await task_service.get_tasks_by_filters({"user_id": "test_user_123"})
            print(f"Found {len(all_tasks)} tasks for user test_user_123")

            return True
        except Exception as e:
            print(f"Error performing database operation: {e}")
            import traceback
            traceback.print_exc()
            return False


if __name__ == "__main__":
    success = asyncio.run(test_database())
    if success:
        print("Database operations are working correctly!")
    else:
        print("Database operations failed.")