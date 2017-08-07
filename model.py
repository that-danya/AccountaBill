"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database;

db = SQLAlchemy()

#####################################################################
# Model definitions


class User(db.Model):
    """User of AccountaBill website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    ponts = db.Column(db.Float, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)


class Goal(db.Model):
    """Goal of user."""

    __tablename__ = "goals"

    goal_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    goal_text = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean)

    # est relationship with User
    user = db.relationship('User', backref='goal')

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Goal goal_id=%s complete=%s>" % (self.goal_id, self.complete)


class Objective(db.Model):
    """Objectives connected to goals of user with duedates."""

    __tablename__ = "objectives"

    obj_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.goal_id'))
    obj_text = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    point_cost = db.Column(db.Float, nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.message_id'))
    img_url = db.Column(db.String(100))

    # est relationship with User
    goal = db.relationship('Goal', backref='objective')
    message = db.relationship('Message_To_Send', backref='objective')

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Objective obj_id=%s complete=%s>" % (self.obj_id, self.complete)


class 



#####################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///accountabill'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
