from flask import Flask, render_template, request, session, redirect, url_for
import utils
import json
import calendar
import datetime

app = Flask(__name__)
app.secret_key = 'dcb61f28eafb8771213f3e0612422b8d'

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
            return redirect(url_for("dashboard/0"))
        else:
            return render_template("login.html")

@app.route("/changepwd", methods=["GET", "POST"])
@app.route("/changepwd/", methods=["GET", "POST"])
def changepwd():
    if request.method == "GET":
        return render_template("changepwd.html")
    else:
        email = request.form['email']
        pwd = request.form['pwd']
        utils.changepwd(email, pwd)
        return redirect(url_for("login"))



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
    if 'logged_in' not in session:
        return redirect(url_for("root"))
    cal = utils.calendardict(0)
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
            return redirect(url_for("view"))


@app.route("/dashboard/<int:page>", methods=["GET", "POST"])
def dashboard(page):
    if 'logged_in' not in session:
        return redirect(url_for("root"))
    cal = utils.calendardict(0)
    cal2 = utils.calendardict2(1)
    if request.method=="GET" and page == 0:
        return render_template("dashboard.html", L = cal)
    if request.method=="GET" and page == 1:
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
            return redirect(url_for("view"))
            #return "You've booked " + session['room'] + " for " + session['day'] + "!"


@app.route("/view", methods=["GET", "POST"])
def view():
    if 'logged_in' not in session:
        return redirect(url_for("root"))
    if request.method=="GET":
        check = list(utils.db.rooms.find({'club': session['email']}))
        today = str(datetime.date.today())
        month = str(today.split('-')[1])
        return render_template("view.html", L = check)
    else:
        info = request.form['del']
        day = info.split(',')[0]
        room = info.split(',')[1]
        club = info.split(',')[2]
        utils.del_room(day, room, club)
        return redirect(url_for("view"))


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
    if request.method=="GET":
        return render_template("del.html")
    else:
        r1 = request.form["room1"]
        r2 = request.form["room2"]
        r3 = request.form["room3"]
        r4 = request.form["room4"]
        r5 = request.form["room5"]
        L = [r1,r2,r3,r4,r5]
        for r in L:
            if len(r) > 2:
                utils.takeoff_room(r)
        return redirect(url_for("add"))



@app.route("/adview", methods=["GET", "POST"])
def adview():
    if request.method=="POST":
        info = request.form['del']
        day = info.split(',')[0]
        room = info.split(',')[1]
        club = info.split(',')[2]
        utils.del_room(day, room, club)
        return redirect(url_for("adview"))
    if request.method == "GET":
        check = list(utils.db.rooms.find())
        newcheck = []
        for item in check:
            if item['club'] != '':
                newcheck.append(item)
        return render_template("adview.html", L = sorted(newcheck, key=lambda k: k['day']))



@app.route("/logout", methods=["GET"])
@app.route("/logout/", methods=["GET"])
def logout():
    session['logged_in'] = False
    return render_template("index.html")


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug=True
    app.run()
