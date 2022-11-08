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
    departures = db.relationship("Flight", backref="origin")
    arrivals = db.relationship("Flight", backref="destination")



    def __str__(self):
        return f"{self.city}, {self.country}, {self.code}"


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String(16))

    def __str__(self):
        return f"{self.name}, {self.number}"

Flight_Day = db.Table(
    "flight_day",
    db.Column("flight_id", db.Integer, db.ForeignKey("flight.id")),
    db.Column("weed_id", db.Integer, db.ForeignKey("week.id"))
)


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
    depart_day = db.relationship("Week", secondary=Flight_Day, backref="flights_of_the_day")
    
    def __str__(self):
        f"{self.id}: {self.origin} to {self.destination}"

