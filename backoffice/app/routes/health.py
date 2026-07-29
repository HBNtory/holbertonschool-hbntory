"""Health check blueprint for the backoffice service."""

from flask import Blueprint
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal

bp = Blueprint("health", __name__)


@bp.route("/health")
def health():
    """Return the service health status, including DB connectivity.

    Runs a lightweight `SELECT 1` to confirm the app can reach the
    database. Used by monitoring and container orchestration.

    Returns:
        a JSON dict and a HTTP status code.
    """
    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}, 200
    except SQLAlchemyError:
        return {"status": "ok", "database": "unreachable"}, 503
