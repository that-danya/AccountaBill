from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Goal, Objective, Message

app = Flask(__name__)

# add key for debug
app.secret_key = 'abc'

# debugger please yell at me if I do something weird
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')


@app.route('/login', methods=['GET'])
def login_user():
    """Login user."""

    ## create user page for login to redirect to.
    return render_template('/login_form.html')


@app.route('/login', methods=['POST'])
def process_login():
    """Process user."""

    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    # don't log in user if not a user name or password match
    if not user:
        flash('No a valid user login.')
        return redirect('/login')
    if user.password != password:
        flash('Incorrect password. Please try again.')
        return redirect('/login')

    # establish session cookie for user
    session['user_id'] = user.user_id

    # Signal to user that they have been logged in.
    flash('You have been logged in!')

    # create user page for login to redirect to user page
    return redirect('/user/%s' % user.user_id)


@app.route('/logout')
def logout_user():
    """Logout user."""

    # Remove cookie from session, signal to user action
    del session['user_id']
    flash('You have been logged out.')

    return redirect('/')


@app.route('/register', methods=['GET'])
def register_form():
    """Show register form for user."""

    ## TODO add hidden form that pipes these in
    # email = request.form['email']
    # password = request.form['password']

    return render_template('/register_form.html')


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form['email']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phonenum']
    points = 10.0

    # Start DB transaction by assigning variables to User class
    new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone, points=points)

    # Commit to DB
    db.session.add(new_user)
    db.session.commit()

    # Flash message confirming add, redirect to home
    ## TODO Change this to redirect to userpage
    flash('User %s added.' % email)

    # redirect to user's page
    return redirect('/user/%s' % user.user_id)


## TODO Need after registrant flow to direct to CREATE GOAL for first time tute
#       that instantiates points with user

@app.route('/user/<int:user_id>')
def user_page(user_id):
    """Show user page"""

    # get user id from db and set to user var
    user = User.query.get(user_id)

    # send user to user_page
    return render_template('user.html', user=user)

## TODO 'BUY' page or Get more points page



####################################################################
# Helper Functions


# if running this page, run debugger, load to host
if __name__ == "__main__":

    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(debug = True, host="0.0.0.0")
