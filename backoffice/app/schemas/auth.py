"""
Pydantic schemas for authentication.
"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """
    Input schema for user authentication.
    """

    email: str
    password: str


class LoginResponse(BaseModel):
    """
    Output schema returned after successful authentication.
    """

    token: str
