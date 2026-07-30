"""Business exceptions related to User entity."""


class UserException(Exception):
    """Base exception for user-related errors."""


class EmailAlreadyExists(UserException):
    """Raised when creating a user with an email already taken."""


class UserNotFound(UserException):
    """Raised when a user is not found."""
