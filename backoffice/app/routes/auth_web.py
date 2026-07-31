"""Web (SSR) authentication: cookie-based login/logout for browsers."""
from datetime import timedelta

from flask import (
    Blueprint, render_template, request, redirect, url_for, make_response,
)
from pydantic import ValidationError

from app.config import Config
from app.exceptions.auth_exceptions import InvalidCredentialsException
from app.schemas.auth import LoginRequest
from app.services.auth_service import AuthService

bp = Blueprint("auth_web", __name__)

ACCESS_COOKIE = "access_token"


@bp.route("/login", methods=["GET", "POST"])
def login():
    """Show the login form (GET) or authenticate + set cookie (POST)."""
    if request.method == "POST":
        try:
            data = LoginRequest(
                email=request.form.get("email"),
                password=request.form.get("password"),
            )
            token = AuthService().login(data)
        except InvalidCredentialsException:
            return render_template(
                "auth/login.html", error="Invalid email or password.",
            )
        except ValidationError:
            return render_template(
                "auth/login.html", error="Please fill in all fields.",
            )

        response = make_response(redirect(url_for("admin.dashboard")))
        response.set_cookie(
            ACCESS_COOKIE,
            token,
            httponly=True,
            samesite="Lax",
            secure=False,  # dev over HTTP; set True behind HTTPS in prod
            max_age=int(
                timedelta(hours=Config.JWT_EXPIRATION_HOURS).total_seconds()
            ),
        )
        return response

    return render_template("auth/login.html")

@bp.route("/logout", methods=["POST"])
def logout():
    """Clear the auth cookie and redirect to the public home."""
    response = make_response(redirect(url_for("web.index")))
    response.delete_cookie(ACCESS_COOKIE)
    return response