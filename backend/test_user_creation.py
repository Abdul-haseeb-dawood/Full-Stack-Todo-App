import asyncio
import uuid
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.db.database import DATABASE_URL

# Create a new database engine for testing
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def test_user_creation():
    async with AsyncSessionLocal() as session:
        # Create user repository and service
        user_repo = UserRepository(session)
        user_service = UserService(user_repo)
        
        # Create a test user
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            password="password123"
        )
        
        print("Attempting to create user...")
        user = await user_service.create_user(user_data)
        
        if user:
            print(f"User created successfully: {user.email}")
            print(f"User ID: {user.id}")
        else:
            print("Failed to create user")
            
            # Check if user already exists
            existing_user = await user_service.get_user_by_email("test@example.com")
            if existing_user:
                print(f"User already exists with email: {existing_user.email}")

if __name__ == "__main__":
    asyncio.run(test_user_creation())