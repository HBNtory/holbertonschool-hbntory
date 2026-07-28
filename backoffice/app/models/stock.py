from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import UniqueConstraint, CheckConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models.branch import Branch


class Stock(Base):
    """Stock quantity of a product at a branch.

    Links a Branch to a product referenced by the Product API's id
    (product_id is an opaque external reference, not a foreign key).
    Unique per (branch_id, product_id); quantity is constrained to be non-negative.
    """
    __tablename__ = "stock"
    __table_args__ = (
        UniqueConstraint("branch_id", "product_id", name="uq_branch_product"),
        CheckConstraint("quantity >= 0", name="ck_quantity_positive")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branches.id"))
    product_id: Mapped[int] = mapped_column()
    quantity: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    branch: Mapped["Branch"] = relationship(back_populates="stock")