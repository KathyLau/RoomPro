import smtplib
from pymongo import MongoClient
import hashlib
import re
from random import randrange
import datetime
from calendar import monthrange
#test

connection = MongoClient("localhost", 27017, connect=False)
db = connection['database']

"""
Returns hashed password
Args:
    text - string to be hashed
Returns:
    hashed string
"""
def hash(text):
    return hashlib.sha256(text).hexdigest()

"""
~~-----------------------------USERS----------------------------------------~~
"""


"""
Checks whether username is allowed
Args:
    username - string to be checked
Returns:
    True if string is allowed
    False if it is not
"""
def check_username(username):
    return not re.search('[^a-zA-Z\s]', username) and len(username) > 0


"""
Registers an user with their email, name, and password.
Args:
    name - club name
    email - user email address
    password - password for the user
Returns:
    True if user does not exist
    False if user already exists
"""
def register_user(name, email, pwd):
    check = list(db.users.find({'email':email}))
    if check == []:
        t = {'name':name, 'email': email, 'pwd': pwd }
        db.users.insert(t)
        return True
    return False


"""
Confirms a user with email and osis.
Args:
    email - club user email address
    pwd - password for the user
Returns:
    True if user exist
    False if user does not exist
"""
def confirm_user(email, pwd):
    check = list(db.users.find({'email':email}))

    if check != []:
        if check[0]['pwd']== pwd:
            return True
    return False


"""
Makes a calendar - dictionary
Args:
    day - day of the week
    date - date of the month
Returns:
    dictionary in day: [dates] format
"""
def calendardict():
    d={}
    today = str(datetime.date.today())
    month = int(today.split('-')[1])
    year = int(today.split('-')[0])
    now = list(monthrange(year, month)) # returns [weekday of first day, number of days]
    currPos = 0
    date = 1
    L = []
    tempL = []
    while currPos < 7:
        if date < 2 and now[0] != currPos:
            tempL += [0]
        else:
            tempL += [date]
            date += 1
        currPos += 1
    L += [tempL]

    tempL = []
    while date < now[1] + 1:
        if len(tempL) == 7:
            L += [tempL]
            tempL = []
        else:
            tempL += [date]
            date +=1
    L += [tempL]
    return L


"""
Adds a locker number to request list
Args:
  f_name: locker holder's name
  u_name: user name
Return:
  True if user exists
  False if user does not exist
"""
def add_request(u_name, f_name):
    check = list(db.users.find({'email':f_name}))

    if check['trade'] != 'no':
        newlist = check[0]['requestL']

        newlist.append(u_name)

        db.users.update(
            {
                'email': f_name
            },
            {'$set':
             {
                 "requestL": newlist
             }
         }
        )
        return True
    return False
