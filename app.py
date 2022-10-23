from flask import Flask

import helper.helper_general as helper_general
import views.login as login
import views.register as register
from helper.helper_limiter import limiter
API_KEY_FILE = "keys.json"
KEYS = helper_general.get_keys(API_KEY_FILE)

def create_app() -> Flask:
    """
    Creates an instance of the Flask web application.
    Returns:
        An instance of the web application with the blueprints configured.
    """
    app = Flask(__name__)
    limiter.init_app(app)
    app.register_blueprint(register.register_blueprint, url_prefix="")
    app.register_blueprint(login.login_blueprint, url_prefix="")

    app.url_map.strict_slashes = False
    app.secret_key = KEYS["app_secret_key"]
    return app


if __name__ == "__main__":
    create_app().run(debug=True)