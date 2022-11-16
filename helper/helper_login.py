"""
Helper functions for the user login system
"""

import bcrypt
from helper.helper_database import create_user, get_userId_by_username
from database import db

def authenticate_password(pwd: str, hashed_pwd: str) -> str:
    """
    Authenticates the password using bcrypt
    Args:
        pwd: the password input by the user in the form.
        hashed_pwd: the pwd stored in the database for the user.
    Returns:
        Whether the pwd mathes the pwd for the user
    """
    return bcrypt.checkpw(pwd.encode("utf-8"), hashed_pwd)

def add_google_user(
    username:str,
    first_name: str,
    last_name: str
):
    """
    Insert the user in the 'account' and 'profile' tables in the database
    Args:
        username: The username input by the user in the form.
        hashed_password: The user's password after hashing.
        first_name: The first name input by the user.
        last_name: The last name input by the user.
    """
    user = create_user(username, "googlegoogle", first_name, last_name)
    print(user)
    db.session.add(user)
    db.session.commit()

def check_username(username):
    if get_userId_by_username(username)== None:
        return True
    return False