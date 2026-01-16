from pydantic import BaseModel, EmailStr, Field
from pydantic.config import ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    is_active: Optional[bool] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLoginResponse(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    message: str = "Login successful"

    model_config = ConfigDict(from_attributes=True)