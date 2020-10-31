from functions import *

import functools

from flaskext.mysql import MySQL
from flask import Flask, render_template, redirect, session, jsonify, request, flash

Type = "Development"

app = Flask(__name__)
app.config.from_object("config." + Type + "Config")

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
### Login & Register & Logout
####################

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login_email = request.form.get('login_mail', "", type=str)
        login_password = request.form.get('login_password', "", type=str)

        # Development
        if Type == "Development":
            print("Login: " + login_email)
            print("Hasło: " + login_password)

        # Logowanie
        if userLogin(login_email, login_password):

            session['isLogged'] = True
            session['user'] = login_email

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!", "type": "danger"})

    return render_template("login.html")


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":

        register_mail = request.form.get('register_mail', "", type=str)
        register_password = request.form.get('register_password', "", type=str)
        register_repeat_password = request.form.get('register_repeat_password', "", type=str)

        # Development
        if Type == "Development":
            print("Login: " + register_mail)
            print("Hasło: " + register_password)
            print("Hasło: " + register_repeat_password)

        # Regex
        if not checkMail(register_mail):
            return jsonify({"title": "", "message": "Prosze wprowadzić poprawny adres E-Mail!"})

        # Sprawdzenie czy hasła są identyczne
        if register_password != register_repeat_password:
            return jsonify({"title": "", "message": "Prosze wprowadzić identyczne hasła!"})

        # Rejestracja
        if userRegister(register_mail, register_password, register_repeat_password):

            session['isLogged'] = True
            session['user'] = register_mail

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!"})

    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('isLogged', None)
    return redirect("/")

####################
### Company
####################

@app.route('/company')
def company():
    return render_template("company.html")


@app.route('/company/add')
@protected
def company_add():
    return render_template("company_add.html")


@app.route('/company/list')
def company_list():
    return render_template("company_list.html")


@app.route('/company/workers')
def company_workers():
    return render_template("company_workers.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
