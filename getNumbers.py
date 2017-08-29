from datetime import datetime
import pytz
from model import User, Objective, connect_to_db
from server import app
from flask import Flask

connect_to_db(app)

with open('numberstotext.txt', 'a') as outFile:
    # define what day's date is in YYYY-MM-DD format
    pacific = pytz.timezone('US/Pacific')
    today = datetime.now(tz=pacific).strftime('%Y-%m-%d')
    print today
    # query db to get all objectives due today
    days_objectives = Objective.query.filter_by(due_date=today).all()
#     # for each obj due, find user phone number
    for each in days_objectives:
        obj = each.obj_id
        print obj
        user = User.query.filter_by(user_id=each.goal.user_id).first()
        print user
        uphone = user.phone
#         # write it to file
        outFile.write('\n' + " " + str(uphone) + " " + str(obj) + " " + today)

    # outFile.write('\n' + today)
