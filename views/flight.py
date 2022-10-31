"""
Handle the view for the ticket search
Available values : ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
"""
from amadeus import Client, Location, ResponseError
from flask import Blueprint, make_response, redirect, render_template, request

flight_blueprint = Blueprint(
    "flight", __name__, static_folder="static", template_folder="templates"
)

API_KEY="oXlnToPyJPj7FqjmXdOGNz1n5d0wEi8C"
API_SECRET="NC1ifmJTqmPLKHIs"

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


@flight_blueprint.route("/flight/search_offers")
def search_offers():
    """
    allow them to search for flights between those locations on the dates they want to travel.
    """
    if request.method == "GET":
        try:
            origin_code = request.args.get("originCode")
            destination_code = request.args.get("destinationCode")
            departure_date = request.args.get("departureDate")
            adults=int(request.args.get("adults", 1))
            children=int(request.args.get("children", 0))
            infants=int(request.args.get("infants", 0))
            travel_class=request.args.get("travelClass","")
            response = amadeus.shopping.flight_offers_search.get(
                originLocationCode=origin_code,
                destinationLocationCode=destination_code,
                departure_date=departure_date,
                adults=adults,
                children=children,
                infants=infants,
                travel_class=travel_class
                )
            context = {
                "data": response.data
            }
            
            return context
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

