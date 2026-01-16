from typing import Optional
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.models.user import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user"""
        return await self.user_repo.create_user(user_data)

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID"""
        return await self.user_repo.get_user_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email"""
        return await self.user_repo.get_user_by_email(email)

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update a user's information"""
        return await self.user_repo.update_user(user_id, user_data)

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        return await self.user_repo.delete_user(user_id)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        return await self.user_repo.authenticate_user(email, password)