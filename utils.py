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
collection = db['rooms']

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
        t = {'name':name, 'email': email, 'pwd': hash(pwd) }
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
        if check[0]['pwd']== hash(pwd):
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
    if now[0] != currPos:
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
    print L
    return L



"""
~~-----------------------------ADMIN------------------------------------~~
"""

"""
Adds rooms to room list 5 at a time
Args:
  r<n>: room number
Return:
  True if succeded
  False if not
"""
def add_room(l):
    for room in l:
        check = list(db.rooms.find({'room': room}))

        today = str(datetime.date.today())
        month = str(today.split('-')[1])
        year = str(today.split('-')[0])
        date = year + '-' + month + '-'
        d = 1

        if  len(room)>2 and check == []:
            while d < 32:
                t = {'day': date + str(d) , 'room':room, 'club': ''}
                d+=1
                db.rooms.insert(t)

"""
adds club name to end of date-room-club
Args:
    d = date
    r = room #
    e = club name
Return:
  True if succeded
  False if not
"""
def book_room(d, r, e):
    check = list(db.rooms.find({'day': d}))
    email(e, "Room Booking", "You are now booked for " + str(r) + " on " + str(d) )
    if check != []:
        db.rooms.update(
            {
                'day': d,
                'room' : r
            },
            {'$set':
             {
                 "club": e
             }
         }
         )
        return True


"""
*admin usage only
change room number of a club
Args:
    d = date
    r = room #
    c = club number
    r2 = new room #
Return:
  True if succeded
  False if not
"""
def change_room(d, r2, c):
    check = list(db.rooms.find({'day': d}))
    if check != []:
        db.rooms.update(
            {
                'day': d,
                'club': c
            },
            {'$set':
             {
                 'room' : r2
             }
         }
         )
        email(c, "Booking Changed", "Your room booking on " + d + " is now in room " + r2)
        return True



"""
change password of an email
Args:
    u = email
    p = password
Return:
  True if succeded
  False if not
"""
def changepwd(u, p):
    check = list(db.users.find({'email': u}))
    if check != []:
        db.users.update(
            {
                'email': u
            },
            {'$set':
             {
                 'pwd' : hash(p)
             }
         }
         )
        email(u, "Password Changed", "Your password is now " + p)
        return True


"""
*admin usage only
cancel a booking
Args:
    d = date
    r = room #
Return:
  True if succeded
  False if not
"""
def del_room(d, r, c):
    check = list(db.rooms.find({'day': d}))
    if check != []:
        db.rooms.update(
            {
                'day': d,
                'room' : r
            },
            {'$set':
             {
                 "club": ''
             }
         }
         )
        email(c, "Booking Cancelled", "Your room booking on " + d + " is now cancelled")
        return True


"""
*admin usage only
take a room off
Args:
    r = room #
Return:
  True if succeded
  False if not
"""
def takeoff_room(r):
    check = list(db.rooms.find({'room': r}))
    if check != []:
        collection.remove({'room' : r})
        return True
    return False


"""
Returns hashed password
Args:
    name - email address to send to
Returns:
    boolean if email was sent
"""
def email(name, subject, message):
  send=True
  TO=name
  SUBJECT= subject
  #randint = str(randrange(1000000000))
  #TEXT="Your user name is " + name + '.' + "Your verification id is " + randint

  TEXT= name + ", " + message

  gmail_sender="dev@stuyclubpub.org"
  gmail_passwd="dev201617"

  server= smtplib.SMTP('smtp.gmail.com',587)
  server.ehlo()
  server.starttls()
  server.ehlo
  server.login(gmail_sender, gmail_passwd)

  BODY='\r\n'.join([
       'To: %s' % TO,
       'From: %s' % gmail_sender,
       'Subject: %s' % SUBJECT,
       '',
       TEXT
       ])

  #if name[-9:]=='@stuy.edu':
  try:
      server.sendmail(gmail_sender, TO, BODY)
      print 'email sent'
      return True
  except:
      print 'Error in sending email'
  #else:
    #print'Please use a stuy.edu email address'
    #send=False
  server.quit()
  return True
  #return send
