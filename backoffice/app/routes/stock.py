from flask import Blueprint

bp = Blueprint("stock", __name__)


@bp.route("/stock")
def test_stock():
    """
    Route to initiate a blueprint for stock api route to connect at
    Flask app factory.
    """
    return {"Test stock": "ok"}
