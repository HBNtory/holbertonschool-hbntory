from sqlalchemy import select

from app import SessionLocal
from app.models.stock import Stock
from app.models.branch import Branch


class StockRepository:
    """Data-access layer for the Stock entity.

    The only place that talks to the ORM for stock. Methods run queries and
    return Stock object (or None), no business logic, no HTTP.
    """

    def create(self, stock: Stock) -> Stock:
        """Persist a new stock row.

        Returns:
            The created Stock, refreshed with its generated id and timestamps.
        """
        local_session = SessionLocal()
        local_session.add(stock)
        local_session.commit()
        local_session.refresh(stock)
        return stock

    def get_by_id(self, stock_id: int) -> Stock:
        """Return a stock row by primary key, or None if not found.

        Returns:
            The matching Stock, or None.
        """
        local_session = SessionLocal()
        return local_session.get(Stock, stock_id)

    def get_by_branch_and_product(
            self,
            branch_id: int,
            product_id: int
    ) -> Stock | None:
        """Return the stock row for a (branch, product) pair, or None.

        Used to renforce the unique (branch_id, product_id) constraint.

        Returns:
            The matching Stock, or None.
        """
        local_session = SessionLocal()
        statement = select(Stock).where(
            Stock.branch_id == branch_id,
            Stock.product_id == product_id,
        )
        return local_session.scalars(statement).first()

    def get_stock_by_branch_label_and_product_id(
            self,
            branch_label: str,
            product_id: int,
    ) -> Stock | None:
        local_session = SessionLocal()

        statement = (
            select(Stock)
            .join(Branch)
            .where(
                Branch.label == branch_label,
                Stock.product_id == product_id,
            )
        )
        return local_session.scalars(statement).first()

    def list(self, branch_id: int | None = None) -> list[Stock]:
        """List stock rows, optionally filtered by branch.

        Returns:
            A list of Stock objects.
        """
        local_session = SessionLocal()
        statement = select(Stock)
        if branch_id is not None:
            statement = statement.where(Stock.branch_id == branch_id)
        return list(local_session.scalars(statement).all())

    def update(self, stock_to_update: Stock) -> Stock:
        """Persist changes made to a stock row by the service.
        Returns:
            The updated Stock, refreshed.
        """
        local_session = SessionLocal()
        local_session.commit()
        local_session.refresh(stock_to_update)
        return stock_to_update

    def delete(self, stock_to_delete: Stock) -> None:
        """Hard-delete a stock row (removes it from the database)."""
        local_session = SessionLocal()
        local_session.delete(stock_to_delete)
        local_session.commit()
