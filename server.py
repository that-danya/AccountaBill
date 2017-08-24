from jinja2 import StrictUndefined

from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Goal, Objective, Message
from twilio import twiml
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse, Body, Message, Redirect
import os

app = Flask(__name__)
app.config.from_object(__name__)

# add key for debug
app.secret_key = 'duuuuude. this is an app!!'

# debugger please yell at me if I do something weird
app.jinja_env.undefined = StrictUndefined


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

    user = User.query.filter_by(email=email).first()

    # don't log in user if not a user name or password match
    if not user:
        flash('Not a valid user login.')
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

    # Start DB transaction by assigning variables to User class
    new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone)

    # Commit to DB
    db.session.add(new_user)
    db.session.commit()

    # Flash message confirming add, redirect to home
    flash('User %s added.' % email)
    session['user_id'] = new_user.user_id

    # redirect to goal page
    return redirect('/goal')


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
        cost = float(request.form.get('goal-points'))
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
    send_welcome_text()
    return redirect('/user/%s' % user)


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
def respond_gotcha_text():
    """Tell user that their message was recieved."""
    # Grab data from Twilio
    user_response = request.form.get("Body")
    print user_response
    user_number = request.form.get("From")
    str_num = str(user_number.strip('+'))
    # user_name = request.values.get('From', None)
    yes = 'YES'
    user_response = str(user_response.upper())
    user_response = user_response.strip(' ')
    if user_response != yes:
        print user_response
    # if user doesn't agree to get texts, change text_confirm + exit function
    if user_response != 'YES':
        user = User.query.filter_by(phone=str_num).first()
        user.text_confirm = False

        print ('User %s does not want to be texted.' % (user.user_id))
        return

    who = who_texted_bill(user_number)
    # Twilio interaction
    response = MessagingResponse()
    message = Message()
    message.body = 'Hello, ' + who + '! I got your message. Thanks for the update!'
    response.append(message)
    response.redirect('gotcha_response.xml', message=message, who=who)

    return str(response)


####################################################################
# Helper Functions


def send_welcome_text():
    """Once user instantiates goal, send welcome_text."""

    # Get user info
    user = session['user_id']
    user = User.query.get(user)
    num = '+' + user.phone

    # Get message info
    welcome = Message.query.get(3)
    body = welcome.message_text

    # Twilio interaction
    welcome_to_send = client.api.account.messages.create(to=num,
                                                         from_=twilio_number,
                                                         body=body)
    return welcome_to_send


def who_texted_bill(phone_number):
    """Query db to find out which user texted a response back via Twilio."""

    texter = User.query.filter_by(phone=phone_number).first()
    if texter is not None:
        name = texter.fname
        return name
    else:
        return 'friend'

# if running this page, run debugger, load to host
if __name__ == "__main__":

    # client = setup_twilio_client()
    connect_to_db(app)
    DebugToolbarExtension(app)
    app.run(debug=True, host="0.0.0.0")
