"""SQLAlchemy model for the Branch entity."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Branch(Base):
    """A company branch, holding stock and linked to user"""
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(100), unique=True)
