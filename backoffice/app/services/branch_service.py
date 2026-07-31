"""
Branch service module.
Contains business logic related to branches.
The service depends on a repository injected from outside.
"""

from app.exceptions.branch_exceptions import (
    BranchNotFoundException,
    DuplicateBranchLabelException, BranchNotEmpty,
)
from app.models.branch import Branch
from app.repositories.branch_repository import BranchRepository
from app.schemas.branch import BranchCreate, BranchUpdate


class BranchService:
    """
    Service layer for Branch business logic.
    """

    def __init__(self, repository: BranchRepository | None = None):
        """
        Initialize service with a repository dependency.

        Args:
            repository: BranchRepository instance.
        """
        self.repository = repository or BranchRepository()

    def create(self, data: BranchCreate) -> Branch:
        """Create a branch. Raises DuplicateBranchLabelException if taken."""
        if self.repository.get_by_label(data.label) is not None:
            raise DuplicateBranchLabelException(data.label)

        branch = Branch(label=data.label)
        return self.repository.create(branch)

    def get(self, branch_id: int) -> Branch:
        """Return a branch by id. Raises BranchNotFoundException if absent."""
        branch = self.repository.get_by_id(branch_id)

        if branch is None:
            raise BranchNotFoundException(branch_id)
        return branch

    def list(self) -> list[Branch]:
        """Return all branches."""
        return self.repository.list()

    def update(self, branch_id: int, data: BranchUpdate) -> Branch:
        """Update the provided fields of a branch (partial update)."""
        branch = self.get(branch_id)
        fields = data.model_dump(exclude_unset=True)

        if "label" in fields:
            existing_branch = self.repository.get_by_label(fields["label"])
            if existing_branch is not None and existing_branch.id != branch.id:
                raise DuplicateBranchLabelException(fields["label"])

        for key, value in fields.items():
            setattr(branch, key, value)

        return self.repository.update(branch)

    def delete(self, branch_id) -> None:
        """Delete a branch by id."""
        branch = self.get(branch_id)
        if branch.users or branch.stock:
            raise BranchNotEmpty(branch_id)
        self.repository.delete(branch)
