"""
Handle the view for the ticket search
Available values : ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
"""
import math
from datetime import datetime

from amadeus import Client, Location, ResponseError
from flask import (Blueprint, make_response, redirect, render_template,
                   request, session)
from helper.helper_api import *
from helper.helper_flight import convert_flight_info, parse_class
from models import Flight, Place, User, Week

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
    try:
        places = Place.query.all()
        filters = []
        q = param.lower()
        for place in places:
            if (q in place.city.lower()) or (q in place.airport.lower()) or (q in place.code.lower()) or (q in place.country.lower()):
                filters.append([place.code, place.city, place.country])
        # response, _ = get_airport_info({"keyword": param, "subType": "AIRPORT"})
        # display at most five list
        # address_information = response.get("data", [])[:5]
        # locations = []
        # for location_info in address_information:
        #     locations.append([location_info.get("iataCode", ""), location_info["address"]["cityName"], location_info["address"]["countryName"]])
        return make_response({"data":filters})
    except ResponseError as error:
        print(error)
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
            if request.args.get("children", ""):
                kwargs.update({"children": int(request.args.get("children", 0))})
            if request.args.get("infants", ""):
                kwargs.update({"infants": int(request.args.get("infants", 0))})
            if request.args.get("travelClass", ""):
                travel_class = parse_class(request.args.get("travelClass", ""))
                kwargs.update({'travelClass': travel_class})
            # print("kwargs = ", kwargs)
            flights, _ = get_ticket_info(kwargs)
            # print(flights)
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


@flight_blueprint.route("/flight/search", methods=["GET", "POST"])
def search_flight():
    username = session.get("username")
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
        
    if request.method == "GET":
        o_place = request.args.get("Origin")
        d_place = request.args.get("Destination")
        trip_type = request.args.get("TripType")
        departdate = request.args.get("DepartDate")
        depart_date = datetime.strptime(departdate, "%Y-%m-%d")
        return_date = None
        seat = request.args.get('SeatClass')
    if request.method == "POST":
        o_place = request.form.get("Origin")
        d_place = request.form.get("Destination")
        trip_type = request.form.get("TripType")
        departdate = request.form.get("DepartDate")
        depart_date = datetime.strptime(departdate, "%Y-%m-%d")
        return_date = None
        seat = request.form.get("SeatClass")


    if trip_type == '2':
        returndate = request.args.get("ReturnDate")
        return_date = datetime.strptime(returndate, "%Y-%m-%d")
        flightday2 = Week.query.filter_by(number=return_date.weekday()).first()
        origin2 = Place.query.filter_by(code=d_place.upper()).first()
        destination2 = Place.query.filter_by(code=o_place.upper()).first()
    
    flightday = Week.query.filter_by(number=depart_date.weekday()).first()
    destination = Place.query.filter_by(code=d_place.upper()).first()
    origin = Place.query.filter_by(code=o_place.upper()).first()
    if seat == 'economy':
        flights = Flight.query.filter_by(depart_day=flightday.id,origin_id=origin.id,destination_id=destination.id).filter(Flight.economy_fare!=0).order_by(Flight.economy_fare).all()
        try:
            max_price = flights[-1].economy_fare
            min_price = flights[0].economy_fare
        except:
            max_price = 0
            min_price = 0
    
        if trip_type == '2':
            flights2 = Flight.query.filter_by(depart_day=flightday2.id,origin_id=origin2.id,destination_id=destination2.id).filter(Flight.economy_fare != 0).order_by(Flight.economy_fare).all()
            try:
                max_price2 = flights2[-1].economy_fare
                min_price2 = flights2[0].economy_fare
            except:
                max_price2 = 0
                min_price2 = 0
    elif seat == 'business':
        flights = Flight.query.filter_by(depart_day=flightday.id,origin_id=origin.id,destination_id=destination.id).filter(Flight.business_fare != 0).order_by(Flight.business_fare).all()
        try:
            max_price = flights[-1].business_fare
            min_price = flights[0].business_fare
        except:
            max_price = 0
            min_price = 0
    
        if trip_type == '2':
            flights2 = Flight.query.filter_by(depart_day=flightday2.id,origin_id=origin2.id,destination_id=destination2.id).filter(Flight.business_fare != 0).order_by(Flight.business_fare).all()
            try:
                max_price2 = flights2[-1].business_fare
                min_price2 = flights2[0].business_fare
            except:
                max_price2 = 0
                min_price2 = 0
    elif seat == "first":
        flights = Flight.query.filter_by(depart_day=flightday.id,origin_id=origin.id,destination_id=destination.id).filter(Flight.first_fare != 0).order_by(Flight.first_fare).all()
        try:
            max_price = flights[-1].first_fare
            min_price = flights[0].first_fare
        except:
            max_price = 0
            min_price = 0
    
        if trip_type == '2':
            flights2 = Flight.query.filter_by(depart_day=flightday2.id,origin_id=origin2.id,destination_id=destination2.id).filter(Flight.first_fare != 0).order_by(Flight.first_fare).all()
            try:
                max_price2 = flights2[-1].first_fare
                min_price2 = flights2[0].first_fare
            except:
                max_price2 = 0
                min_price2 = 0
    if trip_type == '2':
        return render_template(
            "search.html",
            user=user, 
            flights=flights,
            origin= origin,
            destination= destination,
            flights2= flights2,   ##
            origin2= origin2,    ##
            destination2= destination2,    ##
            seat= seat.capitalize(),
            trip_type= trip_type,
            depart_date= depart_date,
            return_date= return_date,
            max_price= math.ceil(max_price/100)*100,
            min_price= math.floor(min_price/100)*100,
            max_price2= math.ceil(max_price2/100)*100,    ##
            min_price2= math.floor(min_price2/100)*100    ##
        )
    else:
        return render_template(
            "search.html", 
            flights= flights,
            origin= origin,
            destination= destination,
            seat= seat.capitalize(),
            trip_type= trip_type,
            depart_date= depart_date,
            return_date= return_date,
            max_price= math.ceil(max_price/100)*100,
            min_price= math.floor(min_price/100)*100
        )
