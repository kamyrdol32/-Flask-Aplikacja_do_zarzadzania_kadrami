from functions import *

import functools

from flaskext.mysql import MySQL
from flask import Flask, render_template, redirect, session, jsonify, request, flash

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

mysql = MySQL()
mysql.init_app(app)

### DECORATOR ###

def protected(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "isLogged" not in session:
            return redirect("/login")
        return func(*args, **kwargs)

    return secure_function

####################
### INDEX
####################

@app.route('/')
@protected
def index():
    return render_template("index.html")

####################
### Login & Register
####################

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login_mail = request.form.get('login_mail', "", type=str)
        login_password = request.form.get('login_password', "", type=str)

        # print("Login: " + login_mail)
        # print("Hasło: " + login_password)

        if userLogin(login_mail, login_password):

            session['isLogged'] = True
            session['user'] = login_mail

            print("Udalo sie")
            print("Zalogowano jako: " + session['user'])

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!", "type": "danger"})

    return render_template("login.html")


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('isLogged', None)
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
