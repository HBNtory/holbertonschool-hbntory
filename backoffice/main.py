from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    debug = Config.FLASK_DEBUG == "1"
    app.run(host="0.0.0.0", port=5000, debug=debug)
