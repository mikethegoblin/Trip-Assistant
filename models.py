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

