from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import BaseModel
from passlib.context import CryptContext
import uuid

# Using argon2 as it's more reliable than bcrypt in some environments
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class User(BaseModel):
    __tablename__ = "users"

    # Using PostgreSQL UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str):
        """Hash and set the user's password"""
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return pwd_context.verify(password, self.password_hash)