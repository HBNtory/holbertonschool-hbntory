"""Health check blueprint for the backoffice service."""

from flask import Blueprint

bp = Blueprint("health", __name__)


@bp.route("/health")
def health():
    """Return the service health status

    Used by monitoring and container orchestration to check that the
    service is up and responding

    Returns:
        a JSON dict and implicit 200 status
    """
    return {"status": "ok"}
