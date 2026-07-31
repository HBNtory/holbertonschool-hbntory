from app.clients.product_client import ProductClient
from app.exceptions.stock_exceptions import (StockAlreadyExists,
                                             StockNotFound,
                                             ProductNotFound)
from app.models.stock import Stock
from app.repositories.stock import StockRepository
from app.schemas.stock import StockCreate, StockUpdate


class StockService:
    """Business logic for stock: uniqueness per (branch, product), CRUD.

    Uses StockRepository for data access (injected). Raises business
    exceptions, it does not deal with HTTP.
    """

    def __init__(
            self,
            repository: StockRepository | None = None,
            product_client: ProductClient | None = None,
    ):
        """Build the service with a repository
        (a default one if none given)."""
        self.repository = repository or StockRepository()
        self.product_client = product_client or ProductClient()

    def create(self, data: StockCreate) -> Stock:
        """Create a stock row for a (branch, product) pair.

        Returns:
            The created Stock.
        """
        if not self.product_client.exists(data.product_id):
            raise ProductNotFound(data.product_id)

        existing = self.repository.get_by_branch_and_product(
            data.branch_id, data.product_id
        )
        if existing is not None:
            raise StockAlreadyExists(data.branch_id, data.product_id)

        stock = Stock(
            branch_id=data.branch_id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        return self.repository.create(stock)

    def list(self, branch_id: int | None = None) -> list[Stock]:
        """Return all stock rows, optionally filtered by branch."""
        return self.repository.list(branch_id)

    def get(self, stock_id: int) -> Stock:
        """Return a stock row by id.

        Returns:
            The matching Stock
        """
        stock = self.repository.get_by_id(stock_id)
        if stock is None:
            raise StockNotFound(stock_id)
        return stock

    def update(self, stock_id: int, data: StockUpdate) -> Stock:
        """Update the provided fields of a stock row (partial update).

        Returns:
            The updated Stock.
        """
        stock = self.get(stock_id)
        fields = data.model_dump(exclude_unset=True)
        for key, value in fields.items():
            setattr(stock, key, value)
        return self.repository.update(stock)

    def delete(self, stock_id: int) -> None:
        """Hard-delete a stock row."""
        stock = self.get(stock_id)
        self.repository.delete(stock)

    def get_stock_by_branch_label_and_product_id(
            self,
            branch_label: str,
            product_id: int,
    ) -> Stock | None:
        return self.repository.get_stock_by_branch_label_and_product_id(
            branch_label=branch_label,
            product_id=product_id,
        )

    def get_stock_by_branch_label(self, branch_label: str):
        return self.repository.get_stock_by_branch_label(branch_label)
