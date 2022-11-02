"""
Handle the view for the ticket search
Available values : ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
"""
from amadeus import Client, Location, ResponseError
from flask import Blueprint, make_response, redirect, render_template, request
from helper.helper_flight import convert_flight_info

flight_blueprint = Blueprint(
    "flight", __name__, static_folder="static", template_folder="templates"
)

API_KEY="RRU3luwDGuknU0Sy16iUXX52G7qCeDnU"
API_SECRET="ASSQQlF8qWj5Vt3F"

amadeus = Client(
    client_id=API_KEY,
    client_secret=API_SECRET
)

@flight_blueprint.route("/flight", methods=["GET"])
def flight():
    return render_template('flight.html')

@flight_blueprint.route("/flight/select_place/<param>", methods=["GET"])
def select_destination(param):
    """
    retrieve airports or cities from the Amadeus Airport & City Search API, 
    allowing a user to choose their origin and destination
    """
    if request.method == "GET":
        try:
            print(param)
            response=amadeus.reference_data.locations.get(
                keyword=param, subType=Location.ANY
            )
            # display at most five list
            address_information = response.data[:5]
            locations = []
            for location_info in address_information:
                locations.append([location_info["iataCode"], location_info["name"],location_info["address"]["cityName"]])
            print(locations)
            return make_response({"data":locations})
        except ResponseError as error:
            print(error)
    else:
        return {"error": "Invalid request method"}

@flight_blueprint.route("/test")
def test():
    return render_template("test_auto.html")


@flight_blueprint.route("/flight/search_offers", methods=["GET"])
def search_offers():
    """
    allow them to search for flights between those locations on the dates they want to travel.
    """
    if request.method == "GET":
        try:
            origin_code = request.args.get("originCode")
            destination_code = request.args.get("destinationCode")
            departure_date = request.args.get("departureDate")
            return_date = request.args.get("returnDate")
            adults=int(request.args.get("adults", 1))
            children=int(request.args.get("children", 0))
            infants=int(request.args.get("infants", 0))
            travel_class=request.args.get("travelClass", "")
            print('fadagsdgdgadfasgdsagadsgd------------------------')
            result = amadeus.shopping.flight_offers_search.get(
        originLocationCode='MAD',
        destinationLocationCode='ATH',
        departureDate='2022-11-01',
        adults=1)
            print("fasdgfhaoshfiadlgdagadsfjdsgioasghadsh")
            print(result, "hi I am the result")
            context = {
                "data": result.data
            }
            # flightInfo = convert_flight_info(context)
            return make_response({"data":result})
            return render_template("flight_display.html", roundTrip=flightInfo)
        except ResponseError as error:
            print(5555555)
            print(error)
    else:
        print(error)
        return {"error": "Invalid request method"}

@flight_blueprint.route("/price_offers")
def price_offer():
    if request.method=="POST":
        try: 
            flight = request.POST['flight']
            response=amadeus.shopping.flight_offers.pricing.post(flight)
            return {"data":response.data}
        except ResponseError as error:
            print(error)
    else:
        return {"error":"Invalid request method"}

