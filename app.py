from flask import Flask, render_template, request, session, redirect, url_for
import utils
import json
import calendar
import datetime

app = Flask(__name__)
app.secret_key = ''

@app.route('/')
def root():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form['name']
        email = request.form["email"]
        pwd = request.form["pwd"]
        utils.register_user(name, email, pwd)
        return redirect(url_for("login"))
    else:
        return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form['email']
        pwd = request.form['pwd']

        if utils.confirm_user(email, pwd):
            session['logged_in'] = True
            session['email'] = email
            session['pwd'] = pwd
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html")

@app.route("/adlogin", methods=["GET", "POST"])
@app.route("/adlogin/", methods=["GET", "POST"])
def adlogin():
    if request.method == "GET":
        return render_template("login.html")
    else:
        email = request.form['email']
        pwd = request.form['pwd']

        if email=="admin" and pwd=="StuySU2017":
            session['logged_in'] = True
            session['email'] = email
            session['pwd'] = pwd
            return redirect(url_for("adview"))
        else:
            return render_template("login.html")



@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    cal = utils.calendardict()
    if request.method=="GET":
        return render_template("dashboard.html", L = cal)
    else:
        d = request.form["day"]
        if len(d)< 3:
            session['day'] = d
            today = str(datetime.date.today())
            month = str(today.split('-')[1])
            year = str(today.split('-')[0])
            date =  year+"-" +month+'-'+d
            session['day'] = date
            check =list(utils.db.rooms.find({'day':date}))
            return render_template("dashboard.html", L = cal, G = check)
        else:
            session['room'] = d
            utils.book_room(session['day'], session['room'], session['email'])
            return "You've booked " + session['room'] + " for " + session['day'] + "!"


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method=="GET":
        #check =list(utils.db.rooms.find({'day': '2016-10-4'}))
        return render_template("add.html") #, L =check)
    else:
        r1 = request.form["room1"]
        r2 = request.form["room2"]
        r3 = request.form["room3"]
        r4 = request.form["room4"]
        r5 = request.form["room5"]
        L = [r1,r2,r3,r4,r5]
        utils.add_room(L)
        return redirect(url_for("add"))


@app.route("/del", methods=["GET", "POST"])
def dele():
    return render_template("del.html")



@app.route("/adview", methods=["GET", "POST"])
def adview():
    return render_template("adview.html")



@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    return render_template("index.html")


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug=True
    app.run()
