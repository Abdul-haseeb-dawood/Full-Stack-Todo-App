#!/usr/bin/env python3
"""
Debug script to test the database connection and task retrieval
"""
import asyncio
import traceback
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session, engine
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


async def debug_get_all_tasks():
    """Debug function to test getting all tasks"""
    print("Starting debug test...")
    
    try:
        # Create a session manually
        async with AsyncSession(engine) as session:
            print("Session created successfully")
            
            # Create repository and service
            task_repo = TaskRepository(session)
            task_service = TaskService(task_repo)
            print("Repository and service created successfully")
            
            # Try to get all tasks
            print("Attempting to get all tasks...")
            tasks = await task_service.get_all_tasks()
            print(f"Successfully retrieved {len(tasks)} tasks")
            
            for i, task in enumerate(tasks):
                print(f"  Task {i+1}: {task.title} (ID: {task.id})")
                
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        

if __name__ == "__main__":
    asyncio.run(debug_get_all_tasks())