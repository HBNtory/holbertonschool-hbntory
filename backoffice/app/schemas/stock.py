from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class StockCreate(BaseModel):
    """Input schema for creating a stock entry."""
    branch_id: int
    product_id: int
    quantity: int = Field(ge=0)


class StockUpdate(BaseModel):
    """Input schema for updating a stock entry."""
    quantity: int | None = Field(default=None, ge=0)


class StockRead(BaseModel):
    """Output schema for returning a stock entry."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    branch_id: int
    product_id: int
    quantity: int
    created_at: datetime
    updated_at: datetime
