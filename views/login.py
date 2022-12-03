"""
Handles the view for the user login system and related functionality.
"""
import os
import pathlib

import google.auth.transport.requests
import helper.helper_login as helper_login
import helper.helper_database as helper_database
import requests
from database import db
from flask import Blueprint, abort, redirect, render_template, request, session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol

GOOGLE_CLIENT_ID = "223412764881-smapie5fi1imh0q1vr9rkldu7nfjrc3u.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json") 

flow = Flow.from_client_secrets_file(  #Flow is OAuth 2.0 a class that stores all the information on how we want to authorize our users
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],  #here we are specifing what do we get after the authorization
    redirect_uri="http://127.0.0.1:5111/callback"  #and the redirect URI is the point where the user will end up after the authorization
)

login_blueprint = Blueprint(
    "login", __name__, static_folder="static", template_folder="templates"
)

def login_is_required(function):  #a function to check if the user is authorized or not
    def wrapper(*args, **kwargs):
        if "google_id" not in session:  #authorization required
            return abort(401)
        else:
            return function()

    return wrapper

@login_blueprint.route("/callback")  #this is the page that will handle the callback process meaning process after the authorization
def callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        abort(500)  #state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request
    )
    print("id_info", id_info)
    user_email = id_info.get("email")
    session["username"] = id_info.get("sub")  #defing the results to show on the page
    session["name"] = id_info.get("name")
    session["first_name"] = id_info.get("given_name")
    session["last_name"] = id_info.get("family_name")
    if helper_login.username_exist(session["username"]) == True:
        helper_database.add_google_user(
                    session["username"],
                    session["first_name"],
                    session["last_name"],
                    user_email
                )
    return redirect("/flight") 

@login_blueprint.route("/", methods=["GET"])
def display_login_page() -> object:
    """
    Renders the login page and validates the user's login details.
    Returns:
         The web page for user login.
    """
    errors = []
    if "username" in session:
        return redirect("/flight")
    else:
        if "error" in session:
            errors = session["error"]
        session["prev-page"] = request.url
        # Clear error session variables.
        session.pop("error", None)
        return render_template("login.html", errors=errors)

@login_blueprint.route("/login")
def google_login():
    """
    google login
    """
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    session["state"] = state
    return redirect(authorization_url)


@login_blueprint.route("/", methods=["POST"])
def login() -> object:
    """
    Validates the user's login details and logs them in.
    Returns:
        Redirection to the main page if login was successful.
    """
    username = request.form.get("username", "").lower()
    password = request.form.get("password", "")

    result = db.session.execute("SELECT password FROM user WHERE username=:usrname;", {"usrname": username}).first()
    # Gets the password if it exists, otherwise returns an error as the
    # username doesn't exist.
    if result:
        hashed_password = result[0]
    else:
        session["error"] = ["login"]
        return render_template("login.html")

    if hashed_password:
        # Checks whether the password is correct for that user.
        if helper_login.authenticate_password(password, hashed_password):
            session["username"] = username
            session["prev-page"] = request.url
            return redirect("/flight")
        else:
            session["error"] = ["login"]
            return render_template("login.html")
    else:
        session["error"] = ["login"]
        return render_template("login.html")

@login_blueprint.route("/logout", methods=["GET", "POST"])
def logout() -> object:
    """
    Logs the user out and redirects them to the home page
    Returns:
        Redirect for the home page
    """
    if "username" in session:
        session.pop("username", None)
    session.clear()

    return redirect("/")
