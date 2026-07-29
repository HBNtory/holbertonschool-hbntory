class EmailAlreadyExists(Exception):
    """Raised when creating a user with an email already taken."""


class UserNotFound(Exception):
    """Raised when a user is not found."""
