from app.exceptions.stock_exceptions import StockAlreadyExist, StockNotFound

from app.models.stock import Stock
from app.repositories.stock import StockRepository
from app.schemas.stock import StockCreate, StockUpdate


class StockService:
    """Business logic for stock: uniqueness per (branch, product), CRUD.

    Uses StockRepository for data access (injected). Raises business
    exceptions, it does not deal with HTTP.
    """

    def __init__(self, repository: StockRepository | None = None):
        """Build the service with a repository (a default one if none given)."""
        self.repository = repository or StockRepository()

    def create(self, data: StockCreate) -> Stock:
        """Create a stock row for a (branch, product) pair.

        Returns:
            The created Stock.
        """
        # TODO: validate product_id against the Product API when integrated.
        existing = self.repository.get_by_branch_and_product(
            data.branch_id, data.product_id
        )
        if existing is not None:
            raise StockAlreadyExist(data.branch_id, data.product_id)

        stock = Stock(
            branch_id=data.branch_id,
            product_id=data.product_id,
            quantity=data.quantity
        )
        return self.repository.create(stock)

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