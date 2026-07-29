"""
Branch repository module.

Contains database access logic for the Branch entity.
This is the only layer that interacts with SQLAlchemy.
"""

from sqlalchemy.orm import Session

from app.models.branch import Branch


class BranchRepository:
    """
    Repository responsible for Branch data access.
    """

    def __init__(self, session: Session):
        """
        Initialize repository with an injected session.

        Args:
            session: SQLAlchemy database session.
        """
        self.session = session

    def create(self, branch: Branch) -> Branch:
        """
        Create a new branch.

        Args:
            branch: Branch ORM object.

        Returns:
            Created branch.
        """

        self.session.add(branch)
        self.session.commit()
        self.session.refresh(branch)

        return branch

    def get_by_id(self, branch_id: int) -> Branch | None:
        """
        Retrieve a branch by its identifier.

        Args:
            branch_id: Branch identifier.

        Returns:
            Branch ORM object or None.
        """

        return self.session.get(
            Branch,
            branch_id,
        )

    def list(
        self,
        label: str | None = None,
    ) -> list[Branch]:
        """
        Retrieve branches with optional filters.

        Args:
            label: Optional label filter.

        Returns:
            List of Branch ORM objects.
        """

        query = self.session.query(Branch)

        if label:
            query = query.filter(
                Branch.label == label
            )

        return query.all()

    def update(self, branch: Branch) -> Branch:
        """
        Update an existing branch.

        Args:
            branch: Branch ORM object.

        Returns:
            Updated branch.
        """

        self.session.commit()
        self.session.refresh(branch)

        return branch

    def delete(self, branch: Branch) -> Branch:
        """
        Delete a branch.

        Args:
            branch: Branch ORM object.

        Returns:
            Deleted branch.
        """

        self.session.delete(branch)
        self.session.commit()

        return branch
