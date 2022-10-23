from models import User

def create_user(
    username:str,
    hashed_pwd: str,
    first_name: str,
    last_name: str
):
    """
    Creates a user object

    :return: user
    """

    user = User(
        username=username,
        password=hashed_pwd,
        first_name=first_name,
        last_name=last_name,
    )

    return user