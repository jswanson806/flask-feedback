from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    """User registration form.
    >>> username = StringField("Username", validators=[InputRequired()])
    >>> password = PasswordField("Password", validators=[InputRequired()])
    >>> email = EmailField("Email", validators=[InputRequired()])
    >>> first_name = StringField("First_name", validators=[InputRequired()])
    >>> last_name = StringField("Last_name", validators=[InputRequired()])
    """

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired()])
    first_name = StringField("First_name", validators=[InputRequired()])
    last_name = StringField("Last_name", validators=[InputRequired()])

class LoginForm(FlaskForm):
    """User login form.
    >>> username = StringField("Username", validators=[InputRequired()])
    >>> password = PasswordField("Password", validators=[InputRequired()])
    """

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback form.
    >>> title = StringField("Title", validators=[InputRequired()])
    >>> content = StringField("Content", validators=[InputRequired()])
    """

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])