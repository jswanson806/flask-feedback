from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask-feedback'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def redirect_to_register():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def user_register_form():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken. Please pick another.')
            return render_template('register.html', form=form)
        session['user_id'] = new_user.username
        return redirect('/secret')
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def user_login_form():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data

        user = User.authenticate(username, password)
        if user:
            session['user_id'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username or password"]
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_details(username):
    if 'user_id' not in session:
        flash("Please login to view that page!")
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    return render_template('user_info.html', user=user)

@app.route('/logout', methods=['POST'])
def logout_user():
    session.pop('user_id')
    flash('Goodbye!')
    return redirect('/login')