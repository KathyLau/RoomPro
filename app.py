from flask import Flask, render_template, request, session, redirect, url_for
import utils
import json
import calendar

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
        utils.register_user(name, email, pwd, num, trade)
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
    return render_template("dashboard.html", L = cal)




@app.route("/adview", methods=["GET", "POST"])
def adview():
    return render_template("adview.html")



@app.route("/logout", methods=["GET"])
def logout():
    session["logged_in"] = False
    return render_template("index.html")


if __name__ == '__main__':
##    app.secret_key = 'dcb61f28eafb8771213f3e0612422b8d'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
    app.run()
