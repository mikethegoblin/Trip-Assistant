""" 
Handles the view for trip destination recommendation
"""
from helper.helper_recommend import get_locations, get_recommendation
from flask import Blueprint, redirect, render_template, request, session
from models import  User
import requests
API_KEY = "AIzaSyBLKr0D_aN8HKMauIPvtUyprO-RXGxpAtw"
API_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
API_url2 = "https://maps.googleapis.com/maps/api/place/photo?"
recommend_blueprint = Blueprint(
    "recommend", __name__, static_folder="static", template_folder="templates"
)

@recommend_blueprint.route("/recommend", methods=["GET"])
def get_recommend_page():
    """
    Render the city recommendation page
    """
    username = session.get("username")
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    locations = get_locations()
    return render_template("recommend.html", result=False, locations=locations, user = user)

@recommend_blueprint.route("/recommend/result", methods=["GET"])
def get_recommend_result():
    """ 
    Render the result of the recommendation
    """
    username = session.get("username")
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    # get form input
    city = request.args.get("location-origin")
    # print(city)
    level1 = request.args.get("tourism-score")
    level2 = request.args.get("food-score")
    level3 = request.args.get("transport-score")
    level4 = request.args.get("internet-score")
    level5 = request.args.get("nightlife-score")


    recommended_city, country, response, table_html, locations = get_recommendation(city, [level1, level2, level3, level4, level5]) 
    params = {
        "key": API_KEY,
        "inputtype": "textquery",
        "fields": "name,photos",
        "input" : recommended_city
    }
    res = requests.get(API_url, params=params).json()
    params = {
            "key": API_KEY,
            "photoreference": res['candidates'][0]['photos'][0]['photo_reference'],
            "maxwidth": res['candidates'][0]['photos'][0]['width'],
            "maxheight": res['candidates'][0]['photos'][0]['height']
        }
    city_picture = requests.get(API_url2, params=params).url
    return render_template("recommend.html",
                            user = user,
                            city_picture = city_picture,
                            result=True,
                            locations=locations,
                            final_city=recommended_city,
                            country=country,
                            response=response,
                            dataframe=table_html,
                            tourism_score=level1,
                            food_score=level2,
                            transport_score=level3,
                            internet_score=level4,
                            nightlife_score=level5)

