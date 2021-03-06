from jinja2 import StrictUndefined
from passlib.apps import custom_app_context as pwd_context
from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Goal, Objective, Message

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse, Body, Message as TMessage, Redirect
import os
import re

app = Flask(__name__)
app.config.from_object(__name__)

# add key for debug
app.secret_key = 'duuuuude. this is an app!!'

# debugger please yell at me if I do something weird
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

# def setup_twilio_client():
#     """Authenticate ID + Token with Twilio to enable access."""

# Pull in id + token from secret.sh
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# Set number = to variable name
twilio_number = os.environ['TWILIO_NUMBER']

# return client


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
    hash = pwd_context.hash(password)
    ok = pwd_context.verify(password, hash)

    user = User.query.filter_by(email=email).first()

    # don't log in user if not a user name or password match
    if not user:
        flash('Not a valid user login.')
        return redirect('/login')
    if not ok:
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

    # Remove cookie from session, signal to user
    del session['user_id']
    flash('You have been logged out.')

    return redirect('/')


@app.route('/register', methods=['GET'])
def register_form():
    """Show register form for user."""

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

    hash = pwd_context.hash(password)

    # Start DB transaction by assigning variables to User class
    new_user = User(email=email, password=hash, fname=fname, lname=lname, phone=phone)

    # Commit to DB
    db.session.add(new_user)
    db.session.commit()

    # Flash message confirming add, redirect to home
    flash('User %s added.' % email)
    session['user_id'] = new_user.user_id

    # redirect to goal page
    return redirect('/carrot')


@app.route('/user/<int:user_id>')
def user_page(user_id):
    """Show user page."""

    if session['user_id'] != user_id:
        return redirect('/user/%s' % session['user_id'])
    else:
        # get user id from db and set to user var
        user = User.query.get(user_id)

        # send user to user_page
        return render_template('user.html', user=user)


## TODO 'BUY' page or Get more points page
@app.route('/carrot', methods=['GET'])
def carrot_form():
    """Show carrot form."""

    # if user is not signed in, redirect home
    if not session['user_id']:
        flash('You have not logged in yet!')
        return redirect('/')

    user = session['user_id']
    user = User.query.get(user)

    # if points < 1:
    #     flash('You do not have enough points to create a new goal! Perhaps complete an objective first?')
    #     return redirect('/user/%s' % session['user_id'])

    return render_template('carrot.html')


@app.route('/carrot_defined', methods=['POST'])
def define_carrot():
    """Process carrot data."""

    # define user
    user = this_user()

    # grab user data from form on /carrot
    earn_this_item = request.form.get('earnThing')
    cost_item = request.form.get('thingCost')

    # interact with db
    # user = User.query.get(user)
    user.earn_thing = earn_this_item
    user.thing_cost = cost_item
    user.points = cost_item

    db.session.commit()

    return redirect('/goal')


@app.route('/goal', methods=['GET'])
def goal_form():
    """Show goal form."""

    # if user is not signed in, redirect home
    if not session['user_id']:
        flash('You have not logged in yet!')
        return redirect('/')

    # if user has no points, redirect to user page
    user = User.query.get(session['user_id'])
    points = user.points
    if points < 1:
        flash('You do not have enough points to create a goal! Perhaps complete an objective first?')
        return redirect('/user/%s' % session['user_id'])

    # render goal page
    return render_template('goal.html', points=points)


@app.route('/define_goal', methods=['POST'])
def render_goal():
    """Process goal data"""

    # est user_id to instantiate Goal/Objectives
    user = session['user_id']

    # goal form data set to variables
    goal_do = request.form.get('goal-action')
    goal_something = request.form.get('goal-noun')
    goal_date = request.form.get('goal-date')
    complete = False

    # concat goal_text
    goal_text = 'I want to ' + goal_do + " " + goal_something + " by " + str(goal_date)

    # Start DB transaction by assigning variables to Goal class
    new_goal = Goal(user_id=user, goal_text=goal_text, complete=complete)

    # Commit goal
    db.session.add(new_goal)
    db.session.commit()
    # define total num of objective rows
    total_objs = int(request.form.get('objCounter'))

    for i in range(1, (total_objs) + 1):
        i = str(i)

        # assign data from from to variables, incremented
        goal_id = new_goal.goal_id
        do = request.form.get('obj-action' + i)
        something = request.form.get('obj-noun' + i)
        daily = request.form.get('obj-check' + i)
        date = request.form.get('obj-date' + i)
        complete = False
        cost = float(request.form.get('points'))
        points = (cost)/total_objs
        message_id = 1

        # concat obj_text
        new_obj_text = 'I will ' + str(do) + " " + str(something)
        if daily:
            new_obj_text += ', daily.'
        else:
            new_obj_text += '.'

        # Start DB transactoin for new Obj, Message, Text
        new_objective = Objective(goal_id=goal_id,
                                  obj_text=new_obj_text,
                                  due_date=date,
                                  complete=complete,
                                  point_cost=points,
                                  message_id=message_id)

    ## TODO: Need to do math for daily

    # DB interaction
        db.session.add(new_objective)

    this_user = User.query.get(user)
    this_user.points = this_user.points - cost

    db.session.commit()

    flash('Your goal was submitted!')
    send_new_goal_text()
    return redirect('/user/%s' % user)

@app.route('/user/<int:user_id>/chart.json')
def get_user_info(user_id):

    if session['user_id'] == user_id:

        user_data = User.query.get(user_id).one()

        return jsonify(user_data.serialize)

@app.route('/user/<int:user_id>.json')
def get_obj_info(user_id):
    """Get objective info."""

    if session['user_id'] == user_id:
        # Query db for all goals for user
        goal_data = Goal.query.filter_by(user_id=user_id).all()

        # create empty dictionary
        objective_dict = {}
        # serialize goals - for json at end of process
        goals = [goal.serialize for goal in goal_data]
        # for every item in goals, query db for objectives
        # put all obj corresponding to a goal in one list
        for g in goal_data:

            obj_data = Objective.query.filter_by(goal_id=g.goal_id).all()
            objective_dict[g.goal_id] = [obj.serialize for obj in obj_data]

        # put into dict to be jsonified
        results = {'goals': goals, 'objectives': objective_dict}

        return jsonify(results)

    else:
        return redirect('/user/%s' % user_id)


@app.route('/user/obj/update.json', methods=['POST'])
def update_objective():
    """Update objection completion in database."""

    obj_id = request.form.get('obj_id')
    completed = request.form.get('complete')
    # user = request.form.get('user_id')

    objective = Objective.query.get(obj_id)
    objective.complete = completed
    obj_cost = objective.point_cost

    objective.goal.user.points = objective.goal.user.points + obj_cost

    db.session.commit()
    return jsonify(objective.serialize), 200


@app.route('/user/goal/update.json', methods=['POST'])
def update_goal():
    """Update goal completion in database."""

    goal_id = request.form.get('goal_id')
    completed = request.form.get('complete')
    # user = request.form.get('user_id')

    goal = Goal.query.get(goal_id)
    goal.complete = completed

    db.session.commit()
    return jsonify(goal.serialize), 200


@app.route('/response', methods=['GET', 'POST'])
def twilio_response():
    """Tell user that their message was recieved."""
    # Grab data from Twilio
    user_response = request.form.get("Body")
    user_number = request.form.get("From")
    who = who_texted_bill(user_number)

    # fit data
    str_num = user_number.strip('+')
    user_response = user_response.upper()
    user_response = user_response.rstrip()
    #  regex for  digits
    obj_match = re.match(r'\d+', user_response, re.I)

    # TODO: include and last message sent = today (if not, else: Sorry! You can only complete on day it's due!!)
    if obj_match:
        # # Twilio interaction
        response = MessagingResponse()
        response.message('Hello, ' + who + '! I got your message. We updated your objective!')

        update_obj_in_db(user_response)

        return str(response)

    # if user doesn't agree to get texts, change text_confirm + exit function
    elif user_response == 'OPT OUT':
        user = User.query.filter(User.phone == str_num, User.fname == who).first()
        user.text_confirm = False
        db.session.commit()

        print ('!!!! *** User %s does not want to be texted. *** !!!!' % (user.user_id))
        # Twilio interaction
        response = MessagingResponse()
        response.message('This will be our last message. Make sure to check off your objectives on the website!')

        return str(response)

    elif user_response == 'YES':
        # Twilio interaction
        response = MessagingResponse()
        response.message('Hello, ' + who + '! I got your message. Thanks for the confirmation!')

        return str(response)

    else:
        # default oops message
        response = MessagingResponse()
        response.message('Didn\'t get that. Please either try again, or log online.')

        return str(response)


####################################################################
# Helper Functions

def this_user():
    """Get user_id from db."""

    user = session['user_id']
    user = User.query.get(user)

    return user


def send_new_goal_text():
    """Once user instantiates goal, send welcome_text."""

    # Get user info
    user = this_user()
    num = '+' + user.phone

    # if user's first time send introduction to Bill
    if len(user.goal) <= 1:
        # Get message info
        welcome = Message.query.get(3)
        body = welcome.message_text
    # otherwise send, I've updated our system!
    else:
        created_message = Message.query.get(2)
        body = created_message.message_text

    # Twilio interaction
    new_message = client.api.account.messages.create(to=num,
                                                     from_=twilio_number,
                                                     body=body)
    return new_message


def who_texted_bill(phone_number):
    """Query db to find out which user texted a response back via Twilio."""

    # fit data
    phone_number = phone_number.strip('+')
    # define user by number
    texter = User.query.filter_by(phone=phone_number).first_or_404()
    # Grab user's first name
    if texter is not None:
        name = texter.fname
        return name
    else:
        return 'friend'


def user_id_of_texter(phone_number):
    """Query db to find out user_id of texter."""

    # fit data
    phone_number = phone_number.strip('+')
    # define user by number
    texter = User.query.filter_by(phone=phone_number).first_or_404()
    # Grab user's first name
    if texter is not None:
        user_id = texter.user_id
        return user_id


def update_obj_in_db(obj_num):
    """Update user's objective in the database."""

    obj = Objective.query.get(obj_num)
    obj.complete = True

    db.session.commit()
    return


# if running this page, run debugger, load to host
if __name__ == "__main__":

    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(debug=True, host="0.0.0.0")
