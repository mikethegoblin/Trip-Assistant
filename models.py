from database import db


class User(db.Model):
    """
    Schema for User table
    """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement="auto")
    username = db.Column(db.String(255), unique=True, nullable=False)
    # email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    last_browsed_country = db.Column(db.String(255), nullable=True)
    tickets = db.relationship("Ticket", backref="user")
    # phone_number = Column(String(10))
    def __repr__(self):
        return f"User {self.username}"

class City(db.Model):
    """
    Schema for City table
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),nullable = False)
    city_ascii = db.Column(db.String(255))
    lat =  db.Column(db.Float)
    lng =  db.Column(db.Float)
    country = db.Column(db.String(255))
    iso2 = db.Column(db.String(255))
    iso3 = db.Column(db.String(255))
    admin_name = db.Column(db.String(255))
    capital = db.Column(db.String(255))
    population = db.Column(db.Integer)
    image = db.Column(db.String(255))


class Place(db.Model):
    """ 
    Schema for Place table
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(64))
    airport = db.Column(db.String(64))
    code = db.Column(db.String(3))
    country = db.Column(db.String(64))
    departures = db.relationship("Flight", backref="origin", foreign_keys="Flight.origin_id")
    arrivals = db.relationship("Flight", backref="destination", foreign_keys="Flight.destination_id")



    def __str__(self):
        return f"{self.city}, {self.country}, {self.code}"


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(16))
    flights_of_the_day = db.relationship("Flight", backref="depart_weekday")

    def __str__(self):
        return f"{self.name}, {self.number}"

# Flight_Day = db.Table(
#     "flight_day",
#     db.Column("flight_id", db.Integer, db.ForeignKey("flight.id")),
#     db.Column("weed_id", db.Integer, db.ForeignKey("week.id"))
# )


class Flight(db.Model):
    """
    Schema for Flight table
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    origin_id = db.Column(db.Integer, db.ForeignKey("place.id"))
    destination_id = db.Column(db.Integer, db.ForeignKey("place.id"))
    depart_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.BigInteger, nullable=True)
    arrival_time = db.Column(db.Time, nullable=False)
    plane = db.Column(db.String(24))
    airline = db.Column(db.String(64))
    economy_fare = db.Column(db.Float, nullable=True)
    business_fare = db.Column(db.Float, nullable=True)
    first_fare = db.Column(db.Float, nullable=True)
    # depart_day = db.relationship("Week", backref="flights_of_the_day", foreign_keys="Week.flight_id")
    depart_day = db.Column(db.Integer, db.ForeignKey("week.id"))
    tickets = db.relationship("Ticket", backref="flight")
    
    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"


class Passenger(db.Model):
    """ 
    Scheme for passenger table
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}, {self.gender}"

TicketPassenger = db.Table(
    "ticket_passenger",
    db.Column("id", db.Integer, autoincrement=True, primary_key=True),
    db.Column("ticket_id", db.Integer, db.ForeignKey('ticket.id')),
    db.Column("passenger_id", db.Integer, db.ForeignKey('passenger.id'))
)

class Ticket(db.Model):
    """
    Schema for Ticket table
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    flight_id = db.Column(db.Integer, db.ForeignKey("flight.id"))
    ref_no = db.Column(db.String(6), nullable=False)
    passengers = db.relationship("Passenger", secondary=TicketPassenger, backref="tickets")
    flight_ddate = db.Column(db.Time, nullable=True)
    flight_adate = db.Column(db.Time, nullable=True)
    flight_fare = db.Column(db.Float, nullable=True)
    other_charges = db.Column(db.Float, nullable=True)
    total_fare = db.Column(db.Float, nullable=True)
    seat_class = db.Column(db.String(20), nullable=False)
    booking_date = db.Column(db.Time, nullable=False)
    mobile = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(45), nullable=False)

    def __str__(self):
        return self.ref_no




