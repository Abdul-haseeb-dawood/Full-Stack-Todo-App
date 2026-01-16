from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID"""
        stmt = select(User).where(User.id == user_id)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address"""
        stmt = select(User).where(User.email == email)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get a user by their username"""
        stmt = select(User).where(User.username == username)
        result = await self.db_session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> Optional[User]:
        """Create a new user"""
        try:
            # Check if user with email already exists
            existing_user = await self.get_user_by_email(user_data.email)
            if existing_user:
                logger.warning(f"User with email {user_data.email} already exists")
                return None
            
            # Check if user with username already exists
            existing_user = await self.get_user_by_username(user_data.username)
            if existing_user:
                logger.warning(f"User with username {user_data.username} already exists")
                return None

            # Create new user
            user = User(
                email=user_data.email,
                username=user_data.username
            )
            user.set_password(user_data.password)

            self.db_session.add(user)
            await self.db_session.commit()
            await self.db_session.refresh(user)
            
            logger.info(f"Created new user with email: {user_data.email}")
            return user
        except IntegrityError as e:
            logger.error(f"Integrity error during user creation: {e}")
            await self.db_session.rollback()
            return None
        except Exception as e:
            logger.error(f"Unexpected error during user creation: {e}")
            await self.db_session.rollback()
            return None

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """Update a user's information"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None

            # Update fields if provided
            if user_data.email is not None:
                user.email = user_data.email
            if user_data.username is not None:
                user.username = user_data.username
            if user_data.is_active is not None:
                user.is_active = user_data.is_active

            await self.db_session.commit()
            await self.db_session.refresh(user)
            return user
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            await self.db_session.rollback()
            return None

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False

            await self.db_session.delete(user)
            await self.db_session.commit()
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            await self.db_session.rollback()
            return False

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        user = await self.get_user_by_email(email)
        if not user or not user.verify_password(password):
            return None
        return user