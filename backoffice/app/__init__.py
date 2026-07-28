from flask import Flask
from app.config import Config
from app.database import SessionLocal


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
    from app.routes.chat import bp as chat_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(chat_bp)

    @app.teardown_appcontext
    def remove_session(exception=None):
        """Automatically closes database sessions when the query is complete"""
        SessionLocal.remove()

    return app
