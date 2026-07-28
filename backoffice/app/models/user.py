from datetime import datetime
import enum
from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy import String, Enum, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.branch import Branch


class UserRole(enum.Enum):
    admin = "admin"
    employee = "employee"


class User(Base):
    """A backoffice user, assigned to a branch, wtih a role and
     login credentials.

    Passwords are stored hashed only (password_hash), never in plain text.
    Deletion is soft: `active` is set to False rather than removing the row.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(Enum(UserRole),
                                           default=UserRole.employee)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    branch: Mapped["Branch"] = relationship(back_populates="users")
