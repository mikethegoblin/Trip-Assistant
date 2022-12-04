"""
Handle the view for the ticket search
Available values : ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
"""
import math
import secrets
from datetime import datetime, timedelta

import pytz
from amadeus import Client, Location, ResponseError
from database import db
from flask import (Blueprint, make_response, redirect, render_template,
                   request, session)
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from helper.helper_api import *
from helper.helper_flight import convert_flight_info, parse_class
from models import (Flight, Passenger, Place, Ticket, TicketPassenger, User,
                    Week)

from views.login import client_secrets_file

flight_blueprint = Blueprint(
    "flight", __name__, static_folder="static", template_folder="templates"
)

FEE = 20.0
flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file=client_secrets_file, scopes=["https://www.googleapis.com/auth/calendar"],
redirect_uri = "http://127.0.0.1:5111/callback2")

@flight_blueprint.route('/logout')
def log_out():
    session.clear()
    return redirect('/login')

@flight_blueprint.route("/flight", methods=["GET"])
def flight():
    # username = session["username"]
    # recommended_cities = get_city_recommendations(username)
    username = session.get("username")
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    args = request.args
    if args:
        return render_template('flight.html', user = user,args = args)
    return render_template('flight.html', user = user)

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
        
        return make_response({"data":filters})
    except ResponseError as error:
        print(error)
    return {"error": "Invalid request method"}

 


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
        seat = request.args.get('SeatClass', 'economy')
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
            user = user,
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

@flight_blueprint.route("/flight/review", methods=["GET"])
def review():
    username = session.get("username")
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    flight_1 = request.args.get("flight1Id")
    date1 = request.args.get("flight1Date")
    seat = request.args.get("seatClass")
    round_trip = False
    if request.args.get("flight2Id"):
        round_trip = True
    
    if round_trip:
        flight_2 = request.args.get("flight2Id")
        date2 = request.args.get("flight2Date")
    
    # if request.user.is_authenticated:
    flight1 = Flight.query.filter_by(id=flight_1).first()
    flight1ddate = datetime(int(date1.split('-')[2]),int(date1.split('-')[1]),int(date1.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
    flight1adate = (flight1ddate + timedelta(microseconds=flight1.duration))
    flight2 = None
    flight2ddate = None
    flight2adate = None
    if round_trip:
        flight2 = Flight.query.filter_by(id=flight_2).first()
        flight2ddate = datetime(int(date2.split('-')[2]),int(date2.split('-')[1]),int(date2.split('-')[0]),flight2.depart_time.hour,flight2.depart_time.minute)
        flight2adate = (flight2ddate + timedelta(microseconds=flight2.duration))
    if round_trip:
        return render_template("book.html", 
            user = user,
            flight1= flight1,
            flight2= flight2,
            flight1ddate= flight1ddate,
            flight1adate= flight1adate,
            flight2ddate= flight2ddate,
            flight2adate= flight2adate,
            seat= seat,
            fee= FEE
        )
    return render_template("book.html", 
        user = user,
        flight1=flight1,
        flight1ddate=flight1ddate,
        flight1adate=flight1adate,
        seat=seat,
        fee=FEE
    )
    # else:
    #     return HttpResponseRedirect(reverse("login"))

@flight_blueprint.route("/flight/payment", methods=["POST"])
def payment():
    username = session.get("username")
    user = None
    if username:
        user = User.query.filter_by(username=username).first()
        #if request.user.is_authenticated:
    ticket_id = request.form['ticket']
    t2 = False
    if request.form.get('ticket2'):
        ticket2_id = request.form['ticket2']
        t2 = True
    fare = request.form.get('fare')
    card_number = request.form['cardNumber']
    card_holder_name = request.form['cardHolderName']
    exp_month = request.form['expMonth']
    exp_year = request.form['expYear']
    cvv = request.form['cvv']

    # try:
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status = 'CONFIRMED'
    ticket.booking_date = datetime.now()
    db.session.commit()
    if t2:
        ticket2 = Ticket.query.filter_by(id=ticket2_id).first()
        ticket2.status = 'CONFIRMED'
        db.session.commit()
        return render_template('payment_process.html', 
            ticket1=ticket,
            ticket2=ticket2,
            user = user
        )
    return render_template('payment_process.html', 
        ticket1=ticket,
        ticket2="",user = user
    )
    

@flight_blueprint.route("/ticket/cancel", methods=["POST"])
def cancel_ticket():
    ref = request.form.get("ref")
    ticket = Ticket.query.filter_by(ref_no = ref).first()
    user_id = ticket.user_id
    username = session["username"]
    ticket_user = User.query.filter_by(id = user_id).first()
    user = User.query.filter_by(username=username).first()
    if ticket_user.id == user.id:
        ticket.status = 'CANCELLED'
        db.session.commit()
        return make_response(
            {'success': True}
        )
    else:
        return make_response(
            {
                'success': False,
                'error': "User unauthorised"
            }
        )
        


@flight_blueprint.route("/flight/ticket/book", methods=["POST"])
def book():
    #if request.user.is_authenticated:
    username = session["username"]
    user = User.query.filter_by(username=username).first()
    flight_1 = request.form.get('flight1')
    flight_1date = request.form.get('flight1Date')
    flight_1class = request.form.get('flight1Class')
    f2 = False
    if request.form.get('flight2'):
        flight_2 = request.form.get('flight2')
        flight_2date = request.form.get('flight2Date')
        flight_2class = request.form.get('flight2Class')
        f2 = True
    countrycode = request.form['countryCode']
    mobile = request.form['mobile']
    email = request.form['email']
    flight1 = Flight.query.filter_by(id=flight_1).first()
    if f2:
        flight2 = Flight.query.filter_by(id=flight_2).first()
    passengerscount = request.form['passengersCount']
    passengers=[]
    for i in range(1,int(passengerscount)+1):
        fname = request.form[f'passenger{i}FName']
        lname = request.form[f'passenger{i}LName']
        gender = request.form[f'passenger{i}Gender']
        psg = Passenger(first_name=fname,last_name=lname,gender=gender.lower())
        passengers.append(psg)
        # passengers.append(Passenger.query.filter_byate(first_name=fname,last_name=lname,gender=gender.lower()))
    coupon = request.form.get('coupon')
    
    ticket1 = createticket(user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile)
    if f2:
        ticket2 = createticket(user,passengers,passengerscount,flight2,flight_2date,flight_2class,coupon,countrycode,email,mobile)

    if(flight_1class == 'Economy'):
        if f2:
            fare = (flight1.economy_fare*int(passengerscount))+(flight2.economy_fare*int(passengerscount))
        else:
            fare = flight1.economy_fare*int(passengerscount)
    elif (flight_1class == 'Business'):
        if f2:
            fare = (flight1.business_fare*int(passengerscount))+(flight2.business_fare*int(passengerscount))
        else:
            fare = flight1.business_fare*int(passengerscount)
    elif (flight_1class == 'First'):
        if f2:
            fare = (flight1.first_fare*int(passengerscount))+(flight2.first_fare*int(passengerscount))
        else:
            fare = flight1.first_fare*int(passengerscount)
    

    if f2:    ##
        return render_template("payment.html",  ##
            user = user,
            fare=fare+FEE,   ##
            ticket= ticket1.id,   ##
            ticket2=ticket2.id   ##
        )  ##
    return render_template("payment.html", 
        user = user,
        fare= fare+FEE,
        ticket= ticket1.id
    )
    #     else:
    #         return HttpResponseRedirect(reverse("login"))
    # else:
    #     return HttpResponse("Method must be form.")

def createticket(user,passengers,passengerscount,flight1,flight_1date,flight_1class,coupon,countrycode,email,mobile):
    print(flight1, "hi create ticket")
    flight1ddate = datetime(int(flight_1date.split('-')[2]),int(flight_1date.split('-')[1]),int(flight_1date.split('-')[0]),flight1.depart_time.hour,flight1.depart_time.minute)
    flight1adate = flight1ddate + timedelta(microseconds=flight1.duration)
    ###################
    ffre = 0.0
    if flight_1class.lower() == 'first':
        flight_fare = flight1.first_fare*int(passengerscount)
        ffre = flight1.first_fare*int(passengerscount)
    elif flight_1class.lower() == 'business':
        flight_fare = flight1.business_fare*int(passengerscount)
        ffre = flight1.business_fare*int(passengerscount)
    else:
        flight_fare = flight1.economy_fare*int(passengerscount)
        ffre = flight1.economy_fare*int(passengerscount)

    # return ticket
    ticket = Ticket(
        user=user,
        ref_no = secrets.token_hex(3).upper(),
        passengers=passengers,
        flight=flight1,
        flight_ddate=flight1ddate,
        flight_adate=flight1adate,
        flight_fare=flight_fare,
        other_charges=FEE,
        total_fare = ffre+FEE+0.0,
        seat_class = flight_1class.lower(),
        status = 'PENDING',
        mobile = ('+'+countrycode+' '+mobile),
        email = email,
    )
    db.session.add(ticket)
    db.session.commit()
    return ticket

@flight_blueprint.route("/flight/getticket")
def get_ticket():
    ref = request.args.get("ref")
    ticket1 = Ticket.query.filter_by(ref_no=ref).first()
    data = {
        'ticket1':ticket1,
        'current_year': datetime.now().year
    }
    return make_response(data)

@flight_blueprint.route("/flight/ticket/api/<ref>")
def ticket_data(ref):
    ticket = Ticket.query.filter_by(ref_no=ref).first()
    print("ticket", ticket)
    return make_response({
        'ref': ticket.ref_no,
        'from': ticket.flight.origin.code,
        'to': ticket.flight.destination.code,
        'flight_date': ticket.flight_ddate,
        'status': ticket.status
    })

@flight_blueprint.route("/bookings")
def list_bookings():
 
    if session.get("username"):
        user = User.query.filter_by(username=session.get("username")).first()
        tickets = Ticket.query.filter_by(user_id=user.id).order_by('booking_date').all()
        print(tickets,"fdsgadafdgsdfd====================")
        return render_template('bookings.html',
            tickets=tickets, user = user
        )
    # else:
    #     return HttpResponseRedirect(reverse('login'))
@flight_blueprint.route("/flight/addevent")
def add_event():
    authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
    departure_date = request.args.get("departure-time")
    arrival_date = request.args.get("arrival-time")
    session["dd1"] = departure_date
    session["dd2"] = arrival_date
    return redirect(authorization_url)

@flight_blueprint.route("/callback2")
def add_to_calendar():
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials
    service = build('calendar', 'v3', credentials=creds)
    dd1 = session["dd1"]
    dd1 = datetime.strptime(dd1, '%Y-%m-%d %H:%M:%S')
    tz1 = pytz.timezone("US/Eastern")
    dd1 = dd1.astimezone(tz1)
    dd2 = session["dd2"]
    dd2 = datetime.strptime(dd2, '%Y-%m-%d %H:%M:%S')
    dd2 = dd2.astimezone(tz1) 
    session.pop("dd1")
    session.pop("dd2")

    event = {
    'summary': 'Flight Information',
    'location': 'Airport',
    'description': 'Your flight info via trip assistant app',
    'start': {
        'dateTime': dd1.isoformat(),
        'timeZone': 'US/Eastern',
        },
    'end': {
        'dateTime': dd2.isoformat(),
        'timeZone': 'US/Eastern',
        },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=1'
        ],
    'attendees': [
        # {'email': 'lpage@example.com'},
        # {'email': 'sbrin@example.com'},
        ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    
    return redirect("/bookings")
