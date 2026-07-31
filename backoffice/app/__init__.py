from flask import Flask
from app.config import Config
from app.database import SessionLocal, Base, engine
from app.models.branch import Branch
from app.models.user import User
from app.models.stock import Stock


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
    from app.routes.web import bp as web_bp

    from app.routes.api.user import bp as api_user_bp
    from app.routes.api.branch import bp as api_branch_bp
    from app.routes.api.stock import bp as api_stock_bp
    from app.routes.api.chat import bp as api_chat_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(branch_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(web_bp)

    app.register_blueprint(api_user_bp)
    app.register_blueprint(api_branch_bp)
    app.register_blueprint(api_stock_bp)
    app.register_blueprint(api_chat_bp)

    @app.teardown_appcontext
    def remove_session(exception=None):
        """Automatically closes database sessions when the query is complete"""
        SessionLocal.remove()

    Base.metadata.create_all(bind=engine)

    return app
