from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Optional

class RegisterForm(FlaskForm):
    """Register a new user form"""

    username = StringField("Username", validators=[InputRequired(message="Username required")])
    password = PasswordField("Password", validators=[InputRequired(message="Password required")])
    email = StringField('Email', validators=[InputRequired(message="Email required")])
    first_name = StringField('First Name', validators=[InputRequired(message="First Name required")])
    last_name = StringField('Last Name', validators=[InputRequired(message="Last Name required")])

class LoginForm(FlaskForm):
    """Login Existing User"""

    username = StringField("username", validators=[InputRequired(message="Username Required")])
    password = StringField("password", validators=[InputRequired(message="Password Required")])

class FeedbackForm(FlaskForm):
    """User feedback submisison form"""

    title = StringField("Title", validators=[InputRequired(message="Title required")])
    content = StringField("Content", validators=[InputRequired(message="Content required")])
