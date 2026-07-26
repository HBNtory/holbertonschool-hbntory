from flask import Blueprint

bp = Blueprint("branch", __name__)


@bp.route("/branch")
def test_branch():
    """
    Route to initiate a blueprint for branch api route to connect at Flask app factory.
    """
    return {"Branch test": "ok"}
