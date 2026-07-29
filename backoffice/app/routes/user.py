from flask import Blueprint

bp = Blueprint("user", __name__)


# To remove when it will implement just to test bp
@bp.route("/users")
def user_test():
    """
    Route to initiate a blueprint for user api route to connect at
     Flask app factory.
    """
    return {"User test": "ok"}
