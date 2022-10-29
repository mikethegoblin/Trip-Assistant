from typing import List, Tuple
from datetime import datetime

import helper.helper_general as helper_general
from flask import Blueprint, redirect, render_template, request, session
from helper.helper_limiter import limiter

main_blueprint = Blueprint(
    "main", __name__, static_folder="static", template_folder="templates"
)

@main_blueprint.route("/main", methods=["GET"])
def display_main_page():
    if "username" in session:
        return render_template("main.html")

    return redirect("/")