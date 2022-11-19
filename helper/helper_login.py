"""
Helper functions for the user login system
"""

import bcrypt
from helper.helper_database import get_userId_by_username
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
def username_exist(username):
    if get_userId_by_username(username)== None:
        return True
    return False