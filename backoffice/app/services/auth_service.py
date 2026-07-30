"""
Authentication service.

Contains business logic related to user authentication.
"""

from app.exceptions.auth_exceptions import (
    InvalidCredentialsException,
)
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest
from app.utils.security import verify_password
from app.utils.token import generate_token


class AuthService:
    """
    Business logic for user authentication.

    Uses UserRepository for data access.
    Raises business exceptions.
    Does not deal with HTTP.
    """

    def __init__(
        self,
        repository: UserRepository | None = None,
    ):
        """Build the service with a repository."""
        self.repository = repository or UserRepository()

    def login(
        self,
        data: LoginRequest,
    ) -> str:
        """
        Authenticate a user.

        Returns:
            JWT authentication token.

        Raises:
            InvalidCredentialsException:
                If the credentials are invalid.
        """

        user = self.repository.get_by_email(data.email)

        if (
            user is None
            or not user.active
            or not verify_password(
                data.password,
                user.password_hash,
            )
        ):
            raise InvalidCredentialsException(
                "Invalid email or password."
            )

        return generate_token(user)
