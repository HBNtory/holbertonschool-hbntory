"""Business exceptions for the Stock entity."""


class StockException(Exception):
    """Base exception for stock-related errors."""


class StockNotFound(StockException):
    """Raised when a stock row is not found."""
    
    def __init__(self, stock_id: int):
        self.stock_id = stock_id
        super().__init__(f"Stock not found: {stock_id}")


class StockAlreadyExist(StockException):
    """Raised when a stock row already exists for a (branch, product) pair."""

    def __init__(self, branch_id: int, product_id: int):
        self.branch_id = branch_id
        self.product_id = product_id
        super().__init__(
            f"Stock already exists for branch {branch_id}, "
            f"product {product_id}"
        )