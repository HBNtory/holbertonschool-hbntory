""" Branch service module.
Contains business logic related to branches.
The service depends on a repository injected from outside.
"""

from app.exceptions.branch_exceptions import (
    BranchNotFoundException,
    DuplicateBranchLabelException,
)


class BranchService:
    """
    Service layer for Branch business logic.
    """

    def __init__(self, repository):
        """
        Initialize service with a repository dependency.

        Args:
            repository: BranchRepository instance.
        """
        self.repository = repository

    def create(self, branch):
        """
        Create a new branch.

        Business rules:
        - Branch label must be unique.

        Args:
            branch: Branch model instance.

        Returns:
            Created branch.

        Raises:
            DuplicateBranchLabelException:
                If label already exists.
        """

        existing_branch = self.repository.get_by_label(
            branch.label
        )

        if existing_branch:
            raise DuplicateBranchLabelException(
                "Branch label already exists"
            )

        return self.repository.create(branch)

    def get(self, branch_id):
        """
        Retrieve a branch by id.

        Args:
            branch_id: Branch identifier.

        Returns:
            Branch instance.

        Raises:
            BranchNotFoundException:
                If branch does not exist.
        """

        branch = self.repository.get(branch_id)

        if branch is None:
            raise BranchNotFoundException(
                "Branch not found"
            )

        return branch

    def list(self):
        """
        Retrieve all branches.

        Returns:
            List of branches.
        """

        return self.repository.list()

    def update(self, branch_id, data):
        """
        Update an existing branch.

        Business rules:
        - Branch label must remain unique.

        Args:
            branch_id: Branch identifier.
            data: Dictionary containing updated values.

        Returns:
            Updated branch.

        Raises:
            BranchNotFoundException:
                If branch does not exist.
            DuplicateBranchLabelException:
                If new label already exists.
        """

        branch = self.get(branch_id)

        if "label" in data:

            existing_branch = self.repository.get_by_label(
                data["label"]
            )

            if (
                existing_branch
                and existing_branch.id != branch.id
            ):
                raise DuplicateBranchLabelException(
                    "Branch label already exists"
                )

            branch.label = data["label"]

        return self.repository.update(branch)

    def delete(self, branch_id):
        """
        Delete a branch.

        Args:
            branch_id: Branch identifier.

        Returns:
            Deleted branch.

        Raises:
            BranchNotFoundException:
                If branch does not exist.
        """

        branch = self.get(branch_id)

        return self.repository.delete(branch)
