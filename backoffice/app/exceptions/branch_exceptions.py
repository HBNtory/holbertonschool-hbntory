"""Business exceptions related to branches."""


class BranchException(Exception):
    """Base exception for branch-related errors."""


class BranchNotFoundException(BranchException):
    """Raised when a branch cannot be found."""


class DuplicateBranchLabelException(BranchException):
    """Raised when a branch label already exists."""


class BranchNotEmpty(BranchException):
    """Raised when deleting a branch that still has users or stock."""