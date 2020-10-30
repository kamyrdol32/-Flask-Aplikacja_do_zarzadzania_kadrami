import functools

from flask import Flask, render_template, redirect, session, jsonify, request

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

### DECORATOR ###

def protected(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "isLogged" not in session:
            return redirect("/login")
        return func(*args, **kwargs)

    return secure_function

### INDEX ###

@app.route('/')
@protected
def index():
    return render_template("index.html")

### LOGOWANIE I REJESTRACJA ###

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        login_mail = request.form.get('login_mail', "", type=str)
        login_password = request.form.get('login_password', "", type=str)
        print("Login:" + login_mail)
        print("Hasło:" + login_password)
        if login_mail == "admin" and login_password == "admin":

            session['isLogged'] = True
            print("Udalo sie")

            return render_template("index.html")
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
