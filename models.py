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
    # phone_number = Column(String(10))


    def __repr__(self):
        return f"User {self.username}"

