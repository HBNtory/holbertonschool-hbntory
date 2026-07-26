from flask import Flask
from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.health import bp as health_bp

    app.register_blueprint(health_bp)

    return app