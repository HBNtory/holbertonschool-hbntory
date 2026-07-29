"""Pydantic schemas for Branch input validation and output serialization."""
from pydantic import BaseModel, ConfigDict


class BranchCreate(BaseModel):
    label: str


class BranchUpdate(BaseModel):
    label: str | None = None


class BranchRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    label: str
