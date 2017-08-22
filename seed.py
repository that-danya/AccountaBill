"""Utility file to seed messages"""

from sqlalchemy import func

from model import User, Goal, Objective, Message, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    # for every row in file, strip and unpack
    for i, row in enumerate(open('seed_data/u.user')):
        row = row.rstrip()
        user_id, email, password, fname, lname, phone, points, text_confirm = row.split('|')

        # declare user
        user = User(user_id=user_id,
                    email=email,
                    password=password,
                    fname=fname,
                    lname=lname,
                    phone=phone,
                    points=points,
                    text_confirm=text_confirm)

        # add to db
        db.session.add(user)

        # provide sense of progress
        if i % 2 == 0:
            print i

    # commit all users to db
    db.session.commit()


def load_goals():
    """Load goals from u.goals into database."""

    # for every row in file, strip and unpack
    for i, row in enumerate(open('seed_data/u.goal')):
        row = row.rstrip()
        goal_id, user_id, goal_text, complete = row.split('|')

        #declare goal
        goal = Goal(goal_id=goal_id,
                    user_id=user_id,
                    goal_text=goal_text,
                    complete=complete)

        # add to db
        db.session.add(goal)

        #provide sense of progress
        if i % 2 == 0:
            print i

    # commit all goals to db
    db.session.commit()


def load_objectives():
    """Load objective from u.objective into database."""

    # for every row in file, strip and unpack
    for i, row in enumerate(open('seed_data/u.objective')):
        row = row.rstrip()
        obj_id, goal_id, obj_text, due_date, complete, point_cost, message_id = row.split('|')

        # declare objective
        objective = Objective(obj_id=obj_id,
                              goal_id=obj_id,
                              obj_text=obj_text,
                              due_date=due_date,
                              complete=complete,
                              point_cost=point_cost,
                              message_id=message_id)

        # add to db
        db.session.add(objective)

        # provide sense of progress
        if i % 2 == 0:
            print i

    # commit all objectives to db
    db.session.commit()


def load_messages():
    """Load messages from u.message into database."""

    # for every row in file, strip and unpack
    for i, row in enumerate(open('seed_data/u.message')):
        row = row.rstrip()
        message_id, message_text = row.split('|')

        # declare message
        message = Message(message_id=message_id,
                          message_text=message_text)

        # add to db
        db.session.add(message)

        # provide sense of progress
        if i % 2 == 0:
            print i

    # commit all messages to db
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_goal_id():
    """Set value for the next goal_id after seeding database"""

    # Get the Max goal_id in the database
    result = db.session.query(func.max(Goal.goal_id)).one()
    max_id = int(result[0])

    # Set the value for the next goal_id to be max_id + 1
    query = "SELECT setval('goals_goal_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_objective_id():
    """Set value for the next obj_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(Objective.obj_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('objectives_obj_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_goals()
    load_objectives()
    load_messages()
    set_val_user_id()
    set_val_goal_id()
    set_val_objective_id()
