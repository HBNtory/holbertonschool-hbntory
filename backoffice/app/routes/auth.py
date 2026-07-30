"""
Authentication routes.
"""

from flask import Blueprint, request

from app.exceptions.auth_exceptions import (
    InvalidCredentialsException,
)
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
)
from app.services.auth import AuthService


bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and return a JWT token.
    """

    service = AuthService()
    data = LoginRequest(**request.get_json())

    try:
        token = service.login(data)

    except InvalidCredentialsException as e:
        return {
            "error": "invalid_credentials",
            "message": str(e),
        }, 401

    response = LoginResponse(token=token)

    return response.model_dump(), 200
