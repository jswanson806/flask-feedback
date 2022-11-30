from flask import Flask, redirect, render_template, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
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
    """Register a new user. 
    --------------------------
     If a user is already logged in, redirects to the user details page.

     Checks for form validation and creates new User instance.

     Trys to commit new_user to the database and redirects to their details page if successful.

     Rerenders the register form if the form is not validated or the user cannot be added to the database.
    
    """
    form = RegisterForm()
    if 'user_id' in session:
        user = session['user_id']
        flash("You are already logged in.")
        return redirect(f'/users/{user}')
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
        return redirect(f'/users/{username}')
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def user_login_form():
    """Logs in a user.
    --------------------
    
    Checks for the user to be in the session already and if so, will redirect to the user details page.

    Checks for form validation calls authenticate() (from the User class) on user if successful.

    Stores information about the user in the session if they are authenticated successfully.

    If validation of the form fails, rerender the login template.

    """
    form = LoginForm()
    if 'user_id' in session:
        user = session['user_id']
        flash("You are already logged in.")
        return redirect(f'/users/{user}')

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
    """Displays user details page.
    -------------------------------
    Checks for the user in the session and redirects to /login if user is not found.

    Renders the user info page if the user is logged in.
    
    """

    if 'user_id' not in session:
        flash("Please login to view that page!")
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    return render_template('user_info.html', user=user)


@app.route('/logout', methods=['POST'])
def logout_user():
    """Logs the user out.
    -------------------------
    Removes the user from the session and redirects to the login page.
    
    """
    
    session.pop('user_id')
    flash('Goodbye!')
    return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Adds feedback from the user.
    ---------------------------------
    Checks for the user in the session and redirects to the user details page if user is not found.

    Checks for form validation and creates a new instance of Feedback class upon validation.

    Adds the new_feedback to the database and commits, then redirect to user details page.

    If validation is not successful, rerenders the feedback form.
    """

    if 'user_id' not in session:
        flash("Please login to view that page!")
        return redirect(f'/users/{username}')

    form = FeedbackForm()
    if form.validate_on_submit():
       title = form.title.data
       content = form.content.data
       new_feedback = Feedback(title=title, content=content, username=username)

       db.session.add(new_feedback)
       db.session.commit()
       return redirect(f'/users/{username}')

    return render_template('add_feedback.html', form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Deletes a user.
    -------------------
    Checks for the user to be in same user in the session.

    Sends delete request to the database.

    Commits and removes the user from the session (logs them out) and redirects to the register page.

    Redirects to the user details page if the user is not the user in the session (not logged in or the wrong user).
    """
    if username == session['user_id']:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('user_id')
        return redirect('/')
    flash("You do not have permission to do that.")
    return redirect(f'/users/{username}')


@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Updates feedback.
    ----------------------
    Checks for the user in the session and redirects to the login page if user is not found (not logged in).

    Creates a new instance of the FeedbackForm class and populates the form with existing data.

    Checks for form validation and commits changes to the database then redirects to the user details page.

    If validation is unsuccessful, rerender the feedback form.
    """
    if 'user_id' not in session:
        flash("Please login to view that page!")
        return redirect('/login')
    
    feedback = Feedback.query.get_or_404(feedback_id)
    # prefill the form with existing data to be editted
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        flash('Feedback updated!')
        return redirect(f'/users/{feedback.username}')
    else:
        return render_template('edit_feedback.html', form=form)


@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Deletes feedback.
    -----------------------
    Checks for the user to be the same user in the session.

    Sends delete request to the database, commits changes, redirects to the user details page.

    If the user is not found in the session (not logged in or the wrong user), redirects to the login page.
    """
    feedback = Feedback.query.get_or_404(feedback_id)
    username = feedback.username
    if username == session['user_id']:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    flash("You do not have permission to do that.")
    return redirect('/login')
