"""Models for user."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
 
db = SQLAlchemy()
 
def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)

# instantiate Bcrypt
bcrypt = Bcrypt()

#user model 
class User(db.Model):
    """User model"""

    __tablename__ = "users"

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    feed = db.relationship('Feedback', backref='users')

    #Start registration
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user"""

        #hash password
        hashed_password = bcrypt.generate_password_hash(password)
        #convert hashed password into utf8 string to store
        hashed_utf8 = hashed_password.decode('utf8')

        #return instance of user with hashed password and everything else.

        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name) 

    #authenticate user
    @classmethod
    def authenticate(cls, username, password):
        """Validate user exist and password is correct
        return user if valid else return false """

        #get user
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return cls(username=username)
        else:
            return False



class Feedback(db.Model):
    """User Feedback Model"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey("users.username"))
    usr = db.relationship('User')




