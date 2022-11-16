""" 
Handles the view for trip destination recommendation
"""
from helper.helper_recommend import get_locations, get_recommendation
from flask import Blueprint, redirect, render_template, request, session

recommend_blueprint = Blueprint(
    "recommend", __name__, static_folder="static", template_folder="templates"
)

@recommend_blueprint.route("/recommend", methods=["GET"])
def get_recommend_page():
    """
    Render the city recommendation page
    """
    locations = get_locations()
    return render_template("recommend.html", result=False, locations=locations)

@recommend_blueprint.route("/recommend/result", methods=["GET"])
def get_recommend_result():
    """ 
    Render the result of the recommendation
    """
    # get form input
    city = request.args.get("location-origin")
    # print(city)
    level1 = request.args.get("tourism-score")
    level2 = request.args.get("food-score")
    level3 = request.args.get("transport-score")
    level4 = request.args.get("internet-score")
    level5 = request.args.get("nightlife-score")


    recommended_city, country, response, table_html, locations = get_recommendation(city, [level1, level2, level3, level4, level5])
    return render_template("recommend.html",
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

