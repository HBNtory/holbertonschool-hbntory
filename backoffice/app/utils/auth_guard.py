"""Auth guards for SSR routes: read the JWT cookie,
 protect pages by login/role."""
from functools import wraps

import jwt
from flask import request, redirect, url_for, g, abort
from app.utils.token import decode_token

ACCESS_COOKIE = "access_token"


def _current_user_payload() -> dict | None:
    """Return the decoded JWT payload from the cookie,
     or None if absent/invalid."""
    token = request.cookies.get(ACCESS_COOKIE)
    if not token:
        return None
    try:
        return decode_token(token)
    except jwt.InvalidTokenError:
        return None


def login_required(view):
    """Redirect to /login if the request has no valid auth cookie."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        payload = _current_user_payload()
        if payload is None:
            return redirect(url_for("auth_web.login"))
        g.user = payload          # {"user_id": ..., "role": ..., ...}
        return view(*args, **kwargs)
    return wrapped


def roles_required(*allowed_roles):
    """Require login AND one of the given roles; else redirect."""
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            payload = _current_user_payload()
            if payload is None:
                return redirect(url_for("auth_web.login"))
            if payload.get("role") not in allowed_roles:
                return redirect(url_for("admin.dashboard"))
            g.user = payload
            return view(*args, **kwargs)
        return wrapped
    return decorator
