"""Pydantic schemas for User input validation and output serialization."""
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.user import UserRole


class UserCreate(BaseModel):
    """Input schema for creating a user
    (plaintext password, hashed by the service).
    """
    first_name: str
    last_name: str
    email: str
    password: str
    branch_id: int
    role: UserRole = UserRole.employee


class UserUpdate(BaseModel):
    """Input schema for updating a user
    (partial, all fields optional).
    """
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    password: str | None = None
    branch_id: int | None = None
    role: UserRole | None = None


class UserRead(BaseModel):
    """Output schema for returning a user.
    Never exposes the password or its hash.
    """
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
    )

    id: int
    first_name: str
    last_name: str
    email: str
    role: UserRole
    active: bool
    branch_id: int
    created_at: datetime
    updated_at: datetime
