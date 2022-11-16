from models import User
from database import db
from models import User, City
import random

DEFAULT_COUNTRIES = ["China", "United States", "Japan", "Germany", "France"]

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

def get_userId_by_username(username):
    return User.query.filter_by(username=username).first()


def get_user_last_browsed_country(username):
    userId = get_userId_by_username(username)
    user = User.query.get(userId)
    if user.last_browsed_country is None:
        return random.choice(DEFAULT_COUNTRIES)
    return user.last_browsed_country

def get_city_info(city):
    city_info = City.query.filter_by(city_ascii=city).first()
    # print(city_info.city_ascii)
    return city_info