from curses.ascii import isalnum
from typing import List, Tuple
from helper.helper_database import create_user, get_userId_by_username
from database import db

import bcrypt


def validate_registration(
    user_name: str,
    first_name: str,
    last_name: str,
    pwd: str,
    pwd_confirm: str,
) -> Tuple[bool, List[str]]:
    """
    Validates the registration details
    Args:
        username: The username input by the user in the form
        first_name: The first name input by the user in the form.
        last_name: The last name input by the user in the form.
        pwd: The password input by the user in the form.
        pwd_confirm: The password confirmation input by the user in the form.
    Returns:
        Whether the registration was valid, and the errors msgs if not.
    """
    valid = True
    message = []

    if (
        user_name == ""
        or first_name == ""
        or last_name == ""
        or pwd == ""
        or pwd_confirm == ""
    ):
        message.append("There are fields have not been filled")
        valid = False
    
    # checks the username only contains valid characters.
    if not user_name.isalnum():
        message.append("Username must only contain letters and numbers")
        valid = False
    
    # checks if user name hasn't been registered
    # TODO

    # checks if the first name and last name don't exceed 20 characters
    if len(first_name) > 20:
        message.append("first name exceeds 20 characters!")
        valid = False
    if len(last_name) > 20:
        message.append("Last name exceeds 20 characters")
        valid = False
    if not all(x.isalpha() or x.isspace() for x in first_name):
        message.append("First name must only contain letters and spaces!")
        valid = False
    if not all(x.isalpha() or x.isspace() for x in last_name):
        message.append("Last name must only contain letters and spaces!")
        valid = False
    
    # Checks that the password has a minimum length of 8 characters, and at
    # least one number.
    if len(pwd) <= 7 or any(char.isdigit() for char in pwd) is False:
        message.append(
            "Password does not meet requirements! It must contain "
            "at least eight characters, including at least one "
            "number."
        )
        valid = False
    # Checks that the passwords match.
    if pwd != pwd_confirm:
        message.append("Passwords do not match!")
        valid = False
    
    # Check username is unique.
    if check_username(user_name) != "True":
        message.append("This username has already been taken!")
        valid = False
    return valid, message

def hash_pwd(password: str) -> str:
    """
    Hashes the password using bcrypt
    Args:
        password: The password input by the user in the form.
    Returns:
        The password after hashing
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password

def register_user(
    username:str,
    hashed_pwd: str,
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
    user = create_user(username, hashed_pwd, first_name, last_name)
    print(user)
    db.session.add(user)
    db.session.commit()

def check_username(username):
    if get_userId_by_username(username)== None:
        return "True"
    return "False"
    
