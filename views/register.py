"""
Handle the view for the user registration system
"""
from flask import Blueprint, redirect, render_template, request, session
from helper import helper_register as helper_register

register_blueprint = Blueprint(
    "register", __name__, static_folder="static", template_folder="templates"
)

@register_blueprint.route("/checkusername", methods=["GET"])
def checkusername():
    username = request.args.get("username")
    if username == "":
         return "False"
    return helper_register.check_username(username)
    
@register_blueprint.route("/register", methods=["GET", "POST"])
def register() -> object:
    """
    Render the user registration page, and registers an account using the user's input from the registration form

    Returns:
        GET: The web page for user registration.
        POST: The web page based on whether the details provided are valid
    """
    if request.method == "GET":
        errors = ""
        if "username" in session:
            return redirect("/flight")
        else:
            if "error" in session:
                errors = session["error"]
            session.pop("error", None)
            session["prev-page"] = request.url
            if "register_details" in session:
                details = session["register_details"]
            else:
                details = ["", "", ""]
            
            return render_template(
                "register.html",
                errors=errors,
                details=details
            )
    
    if request.method == "POST":
        user_name = request.form.get('username', "").lower()
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        pwd = request.form.get('password1', "")
        pwd_confirm = request.form.get('password2', "")
        
        valid, msg = helper_register.validate_registration(
            user_name,
            first_name,
            last_name,
            pwd,
            pwd_confirm,
        )
        # register the user if details are valid
        if valid:
            # hash the pwd usign bcrypt
            hashed_pwd = helper_register.hash_pwd(pwd)
            helper_register.register_user(
                user_name,
                hashed_pwd,
                first_name,
                last_name
            )
            session['username'] = user_name
            return redirect("/register")
        else:
            details = [user_name, first_name, last_name]
            session["register_details"] = details
            session["error"] = msg
            return redirect("/register")

    