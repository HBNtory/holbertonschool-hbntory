"""
JWT token utilities.

Provides helper functions to generate and decode JSON Web Tokens (JWT).
This module is framework-agnostic and can be reused outside Flask.
"""

from datetime import datetime, timedelta, timezone

import jwt

from app.config import Config
from app.models.user import User

JWT_ALGORITHM = "HS256"


def generate_token(user: User) -> str:
    """
    Generate a signed JWT for an authenticated user.

    Args:
        user: Authenticated User instance.

    Returns:
        Encoded JWT string.
    """

    now = datetime.now(timezone.utc)

    payload = {
        "user_id": user.id,
        "role": user.role.value,
        "iat": now,
        "exp": now + timedelta(
            hours=Config.JWT_EXPIRATION_HOURS
        ),
    }

    return jwt.encode(
        payload,
        Config.JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT.

    Args:
        token: JWT string.

    Returns:
        Decoded JWT payload.

    Raises:
        jwt.InvalidTokenError:
            If the token is invalid or expired.
    """

    return jwt.decode(
        token,
        Config.JWT_SECRET_KEY,
        algorithms=[JWT_ALGORITHM],
    )
