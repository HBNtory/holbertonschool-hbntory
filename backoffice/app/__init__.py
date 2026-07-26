from flask import Flask
from app.config import Config


def create_app():
    """Build and return a configured Flask application.

    Application factory: constructs a fresh app instead of a module-level
    global, so it can be created with different configs and to avoid circular
    imports when registering blueprints.

    Returns:
        the configured application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.health import bp as health_bp
    from app.routes.user import bp as user_bp
    from app.routes.branch import bp as branch_bp
    from app.routes.stock import bp as stock_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(stock_bp)

    return app
