import os


class Config:
    """
    A Config class which read environment when it's load.
    No methods only attributes.
    """
    FLASK_DEBUG = os.environ['FLASK_DEBUG']

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ['MYSQL_USER']}:"
        f"{os.environ['MYSQL_PASSWORD']}"
        f"@{os.environ['MYSQL_HOST']}:{os.environ['MYSQL_PORT']}"
        f"/{os.environ['MYSQL_DATABASE']}"
    )

    # External Product API
    PRODUCT_API_URL = os.environ['PRODUCT_API_URL']

    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

    JWT_EXPIRATION_HOURS = int(
        os.environ.get("JWT_EXPIRATION_HOURS", "24")
    )
    # SEED ADMIN CREDENTIALS
    ADMIN_BACKOFFICE_EMAIL = os.environ['ADMIN_BACKOFFICE_EMAIL']
    ADMIN_BACKOFFICE_PASSWORD = os.environ['ADMIN_BACKOFFICE_PASSWORD']
