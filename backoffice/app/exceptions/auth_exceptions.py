"""
Authentication exceptions.

Contains business exceptions related to user authentication.
"""


class AuthenticationException(Exception):
    """
    Base exception for authentication errors.
    """


class InvalidCredentialsException(AuthenticationException):
    """
    Raised when authentication credentials are invalid.
    """
