from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_async_session
from app.schemas.user import UserCreate, UserLogin, UserLoginResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from typing import Dict

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_service(db_session: AsyncSession = Depends(get_async_session)):
    """Dependency to get the user service with repository"""
    user_repo = UserRepository(db_session)
    return UserService(user_repo)


@router.post("/signup", response_model=UserLoginResponse, status_code=201)
async def signup(
    user_create: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user"""
    try:
        # Check if user already exists
        existing_user = await user_service.get_user_by_email(user_create.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists"
            )

        # Create new user
        user = await user_service.create_user(user_create)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create user"
            )

        # Return user info (without password)
        return UserLoginResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@router.post("/signin", response_model=UserLoginResponse)
async def signin(
    user_login: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    """Authenticate a user and return user info"""
    try:
        # Authenticate user
        user = await user_service.authenticate_user(user_login.email, user_login.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )

        # Return user info (without password)
        return UserLoginResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )


@router.post("/signout")
async def signout():
    """Simple signout endpoint - no session management needed for this basic implementation"""
    return {"message": "Successfully signed out"}