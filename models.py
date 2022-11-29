from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User model
    >>> username = db.Column(db.String(length=20), primary_key=True)
    >>> password = db.Column(db.String, nullable=False)
    >>> email = db.Column(db.String(length=50), nullable=False, unique=True)
    >>> first_name = db.Column(db.String(length=30), nullable=False)
    >>> last_name = db.Column(db.String(length=30), nullable=False)
    """

    __tablename__ = 'users'

    username = db.Column(db.String(length=20), primary_key=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    first_name = db.Column(db.String(length=30), nullable=False)
    last_name = db.Column(db.String(length=30), nullable=False)

    def __repr__(self):
        return f"<User {self.username} email {self.email} firstname {self.first_name} lastname {self.last_name}>"

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        
        Return user if valid; else return False
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback model
    
    >>>
    >>>
    >>>
    >>>
    >>>
    """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(length=100), nullable=False)
    content = db.Column(db.String, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)

    user = db.relationship('User', backref="feedback", single_parent=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Feedback ID {self.id} title {self.title} username {self.username}>"