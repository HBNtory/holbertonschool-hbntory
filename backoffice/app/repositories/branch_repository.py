"""
Branch repository module.

Contains database access logic for the Branch entity.
This is the only layer that interacts with SQLAlchemy.
"""

from sqlalchemy import select

from app.database import SessionLocal
from app.models.branch import Branch


class BranchRepository:
    """
    Repository responsible for Branch data access.
    """

    def create(self, branch: Branch) -> Branch:
        """
        Create a new branch.

        Args:
            branch: Branch ORM object.

        Returns:
            Created branch.
        """
        local_session = SessionLocal()
        local_session.add(branch)
        local_session.commit()
        local_session.refresh(branch)
        return branch

    def get_by_id(self, branch_id: int) -> Branch | None:
        """
        Retrieve a branch by its identifier.

        Args:
            branch_id: Branch identifier.

        Returns:
            Branch ORM object or None.
        """
        local_session = SessionLocal()
        return local_session.get(
            Branch,
            branch_id,
        )

    def get_by_label(self, label: str) -> Branch | None:
        """Return a branch by label, or None if not found."""
        local_session = SessionLocal()
        statement = select(Branch).where(Branch.label == label)
        return local_session.scalars(statement).first()

    def list(
        self,
    ) -> list[Branch]:
        """
        Retrieve branches with optional filters.

        Returns:
            List of Branch ORM objects.
        """

        local_session = SessionLocal()
        statement = select(Branch)
        return list(local_session.scalars(statement).all())

    def update(self, branch: Branch) -> Branch:
        """
        Update an existing branch.

        Args:
            branch: Branch ORM object.

        Returns:
            Updated branch.
        """

        local_session = SessionLocal()
        local_session.commit()
        local_session.refresh(branch)
        return branch

    def delete(self, branch: Branch) -> None:
        """
        Delete a branch.

        Args:
            branch: Branch ORM object.

        Returns:
            Deleted branch.
        """
        local_session = SessionLocal()
        local_session.delete(branch)
        local_session.commit()
