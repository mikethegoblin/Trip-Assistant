from flask import Flask
from flask_migrate import Migrate

import helper.helper_general as helper_general
import views.flight as flight
import views.login as login
import views.register as register
from database import db
from helper.helper_limiter import limiter

API_KEY_FILE = "keys.json"
KEYS = helper_general.get_keys(API_KEY_FILE)
from models import *
import os

migrate = Migrate()
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

def create_app() -> Flask:
    """
    Creates an instance of the Flask web application.
    Returns:
        An instance of the web application with the blueprints configured.
    """
    app = Flask(__name__)
    app.register_blueprint(register.register_blueprint, url_prefix="")
    app.register_blueprint(login.login_blueprint, url_prefix="")
    app.register_blueprint(flight.flight_blueprint, url_prefix="")

    app.url_map.strict_slashes = False
    app.secret_key = KEYS["app_secret_key"]
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.init_app(app)
    # handles database migrations
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()  # Create database tables for our data models

    return app


if __name__ == "__main__":
    app = create_app()
    # app.run()
    app.run(host = "0.0.0.0", port = 5111, debug=True)
