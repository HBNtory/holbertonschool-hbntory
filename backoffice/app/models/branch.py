"""SQLAlchemy model for the Branch entity."""
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models.user import User
    from app.models.stock import Stock


class Branch(Base):
    """A company branch, holding stock and linked to user"""
    __tablename__ = "branches"

    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(100), unique=True)

    users: Mapped[list["User"]] = relationship(back_populates="branch")
    stock: Mapped[list["Stock"]] = relationship(back_populates="branch")
