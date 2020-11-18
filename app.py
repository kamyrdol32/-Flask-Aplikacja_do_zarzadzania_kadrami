from functions import *

import functools

from flaskext.mysql import MySQL
from flask import Flask, render_template, redirect, session, jsonify, request, flash

####################
### CONFIG & DECORATOS
####################

Type = "Development" # Production or Development

# Pobieranie config'a z pliku config.py
app = Flask(__name__)
app.config.from_object("config." + Type + "Config")

# Aktywowanie modułu MySQL
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
        login_mail = request.form.get('login_mail', "", type=str)
        login_password = request.form.get('login_password', "", type=str)

        # Development
        if Type == "Development":
            print("Logowanie Login: " + login_mail)
            print("Logowanie Hasło: " + login_password)

        # Logowanie
        if userLogin(login_mail, login_password):

            session['isLogged'] = True
            session['user'] = login_mail
            session['ID'] = getUserID(login_mail)

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

        register_firstname = request.form.get('register_firstname', "", type=str)
        register_lastname = request.form.get('register_lastname', "", type=str)

        # Development
        if Type == "Development":
            print("Rejestracaja Login: " + register_mail)
            print("Rejestracaja Hasło: " + register_password)
            print("Rejestracaja Hasło: " + register_repeat_password)

        # Weryfikacja danych
        # if not check("Mail", register_mail):
        #     return jsonify({"title": "", "message": "Prosze wprowadzić poprawny adres E-Mail!"})

        # Sprawdzenie czy hasła są identyczne
        if register_password != register_repeat_password:
            return jsonify({"title": "", "message": "Prosze wprowadzić identyczne hasła!"})

        # Rejestracja
        if userRegister(register_mail, register_password, register_repeat_password, register_firstname, register_lastname):

            session['isLogged'] = True
            session['user'] = register_mail
            session['ID'] = getUserID(register_mail)

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!"})

    return render_template("register.html")


@app.route('/logout')
@protected
def logout():
    session.pop('isLogged', None)
    session.pop('user', None)
    session.pop('ID', None)
    return redirect("/")

####################
### Company
####################

@app.route('/company')
@protected
def company():
    return render_template("company.html")


@app.route('/company/add', methods=['POST', 'GET'])
@protected
def company_add():
    if request.method == 'POST':

        company_add_name = request.form['company_add_name']
        company_add_nip = request.form['company_add_nip']
        company_add_regon = request.form['company_add_regon']
        company_add_street = request.form['company_add_street']
        company_add_city = request.form['company_add_city']
        company_add_zip = request.form['company_add_zip']
        company_add_state = request.form['company_add_state']
        company_add_phone = request.form['company_add_phone']
        company_add_mail = request.form['company_add_mail']

        if checkCompany(company_add_name, company_add_nip, company_add_regon):
            return jsonify({"title": "", "message": "Podana firma jest już w rejestrze lub podany NIP/Regon jest juz zarejstrowany!"})

        if companyRegister(getUserID(session['user']), company_add_name, company_add_nip, company_add_regon, company_add_street, company_add_city, company_add_zip, company_add_state, company_add_phone, company_add_mail):
            return jsonify({"redirect": "/"})

    return render_template("company_add.html", States=getStates())


@app.route('/company/list')
@app.route('/company/list/<int:ID>')
@protected
def company_list(ID=False):

    CompaniesList = getUserCompaniesList(session['ID'])

    if not ID and CompaniesList:
        ID = CompaniesList[0][0]

    if not CompaniesList:
        return redirect("/company/add")

    CompaniesData = getCompanyData(ID)

    return render_template("company_list.html", SelectedID=ID, CompaniesList=CompaniesList, CompaniesData=CompaniesData)


@app.route('/company/workers')
@app.route('/company/workers/<int:ID>')
@protected
def company_workers(ID=False):

    Companies = getUserCompaniesList(session['ID'])

    if not ID and Companies:
        ID = Companies[0][0]

    if not Companies:
        return redirect("/company/add")

    UsersData = []

    WorkersList = getCompanyWorkersID(ID)
    for WorkerID in WorkersList:

        print("ID: " + str(ID))
        print("WorkerID: " + str(WorkerID[0]))

        # Pobieranie danych dotyczących pracownika
        UserData = getUserData(WorkerID[0])
        UserCompanyData = getCompanyUserData(ID, WorkerID[0])

        User = []

        for Data in UserData:
            User.append(Data)

        for Data in UserCompanyData:
            User.append(Data)

        # Tworznie 2D tabeli
        UsersData.append(User)

    print(UsersData)

    return render_template("company_workers.html", UserID=session['ID'], SelectedID=ID, CompaniesNames=Companies, UsersData=UsersData)


@app.route('/company/workers/details')
@app.route('/company/workers/details/<int:ID>')
@protected
def company_workers_details(ID=False):

    Companies = getUserCompaniesList(session['ID'])

    if not ID and Companies:
        ID = Companies[0][0]

    if not Companies:
        return redirect("/company/add")

    # Pobieranie danych dotyczących pracownika
    UserData = getUserData(ID)

    return render_template("company_workers_details.html", UserData=UserData)


@app.route('/company/workers/edit')
@app.route('/company/workers/edit/<int:ID>')
@protected
def company_workers_edits(ID=False):
    return render_template("company_workers_edits.html")


@app.route('/company/workers/add')
@protected
def company_workers_add():
    return render_template("company_workers_add.html")


@app.route('/company/vacation/')
@protected
def company_workers_vacations():
    return render_template("company_workers_vacations.html")

####################
### Account
####################

@app.route('/account/')
@protected
def account():
    return render_template("account.html")


@app.route('/account/password')
@protected
def account_password():
    return render_template("account_password.html")\


@app.route('/account/edit')
@protected
def account_edit():
    return render_template("account_edit.html")

####################
### Messages
####################

@app.route('/messages', methods=['POST', 'GET'])
@app.route('/messages/<int:ID>', methods=['POST', 'GET'])
@protected
def messages(ID=False):
    if request.method == "POST" and ID:

        messages_message = request.form.get('message', "", type=str)

        if sendMessage(session['ID'], ID, messages_message):
            return jsonify({"sendMessage": "true"})

    IDs = getMessagesListUsersID(session['ID']) or False
    if IDs:
        NameSurname = getMessagesBasicData(session['ID'], IDs)
        LatestMessages = getLatestMessages(session['ID'], IDs)

        Table = []

        for key, NR in enumerate(IDs):
            Data = [NameSurname[key][0], NameSurname[key][1], NameSurname[key][2], LatestMessages[key][0], LatestMessages[key][1], LatestMessages[key][2]]
            Table.append(Data)

        if ID:
            Messages = getMessages(session['ID'], ID)

            return render_template("messages.html", Table=Table, ID=session['ID'], Messages=Messages)
        else:
            return render_template("messages.html", Table=Table)
    else:
        return jsonify({"title": "", "message": "Nie posiadasz żadnych wiadomości!"}) # Naprawic

####################
### Others
####################


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)
