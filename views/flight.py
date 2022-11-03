"""
Handle the view for the ticket search
Available values : ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
"""
from amadeus import Client, Location, ResponseError
from flask import Blueprint, make_response, redirect, render_template, request
from helper.helper_api import *
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
            response, _ =get_airport_info({"keyword": param, "subType": "AIRPORT"})
            # display at most five list
            address_information = response.get("data", [])[:5]
            locations = []
            for location_info in address_information:
                locations.append([location_info.get("iataCode", ""), location_info["address"]["cityName"], location_info["address"]["countryName"]])
            return make_response({"data":locations})
        except ResponseError as error:
            print(error)
    else:
        return {"error": "Invalid request method"}

@flight_blueprint.route("/flight/search_offers", methods=["GET"])
def search_offers():
    """
    allow them to search for flights between those locations on the dates they want to travel.
    """
    if request.method == "GET":
        try:
            kwargs = {'originLocationCode' : request.args.get("originLocationCode"),
            'destinationLocationCode' : request.args.get("destinationLocationCode"),
            'departureDate' : request.args.get("departureDate"),
            'adults':int(request.args.get("adults", 1)),
            "max": 10}
            if request.args.get("returnDate", ""):
                kwargs.update({'returnDate' :request.args.get("returnDate", "")})
            if int(request.args.get("children", 0)):
                kwargs.update({"chilren": int(request.args.get("children", 0))})
            if int(request.args.get("infants", 0)):
                kwargs.update({"infants": int(request.args.get("infants", 0))})
            if request.args.get("travelClass", ""):
                kwargs.update({'travelClass':request.args.get("travelClass", "")})
            flights, _ = get_ticket_info(kwargs)
            flight_offers = convert_flight_info(flights.get("data", []))
            return render_template("flight_display.html", flight_offers=flight_offers, oneway = request.args.get("returnDate", "") == "")
        except ResponseError as error:
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

@flight_blueprint.route("/trip_purpose_prediction", methods = ["GET"])
def predict_trip():
    """
    If a traveler has shown interest in Berlin, what other destinations would he/she like?
    """
    kwargs = {'originLocationCode': request.args.get('Origin'),
            'destinationLocationCode': request.args.get('Destination'),
            'departureDate': request.args.get('Departuredate'),
            'returnDate': request.args.get('Returndate')}
    
    try:
        purpose = amadeus.travel.predictions.trip_purpose.get(
            **kwargs).data['result']

    except ResponseError as error:
        print(error)
        return render_template(request, 'home.html', {})
    return render_template(request, 'home.html', {'res': purpose})
