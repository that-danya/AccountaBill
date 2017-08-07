from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

#from model import connect_to_db, db, User, Goal, Objective, Message, DebugToolbarExtension

app = Flask(__name__)

# add key for debug
app.secret_key = 'abc'

# debugger please yell at me if I do something weird
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template('homepage.html')


@app.route('/login')
def login_user():
    """Login user."""

    ## create user page for login to redirect to.
    return render_template('/login.html')


@app.route('/logout')
def logout_user():
    """Logout user."""

    # Remove cookie from session, signal to user action
    del session['user_id']
    flash('You have been logged out.')

    return redirect('/')


@app.route('/register', methods='[GET]')
def register_form():
    """Show register form for user."""

    ## TODO add hidden form that pipes these in
    # email = request.form['email']
    # password = request.form['password']

    return render_template('/register_form.html')

@app.route('/register', methods='[POST]')
def register_process():
    """Process registration."""

    # Get form variables
    fname = request.form['fname']
    lname = request.form['lname']
    phone = request.form['phonenum']

    # Start DB transaction by assigning variables to User class
    new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone)

    # Commit to DB
    db.session.add(new_user)
    db.session.commit()

    # Flash message confirming add, redirect to home
    ## TODO Change this to redirect to userpage
    flash('User %s added.' % email)
    return redirect('/')



####################################################################
# Helper Functions


# if running this page, run debugger, load to host
if __name__ == "__main__":

    app.run(debug = True, host="0.0.0.0")
