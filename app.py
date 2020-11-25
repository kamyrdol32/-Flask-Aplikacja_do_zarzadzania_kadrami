from functions import *

import functools

from flaskext.mysql import MySQL
from flask_mail import Mail, Message
from flask import Flask, render_template, redirect, session, jsonify, request, flash

####################
### CONFIG & DECORATOS
####################

Type = "Development" # Production or Development

# Pobieranie config'a z pliku config.py
app = Flask(__name__)
app.config.from_object("config." + Type + "Config")

# Aktywowanie modułu MySQL & Mail
mysql = MySQL()
mysql.init_app(app)
mail = Mail(app)

### DECORATOR ###

def protected(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if "isLogged" not in session:
            flash("Odmowa dostępu!")
            return redirect("/login")
        if "user" not in session:
            flash("Odmowa dostępu!")
            return redirect("/login")
        if "ID" not in session:
            flash("Odmowa dostępu!")
            return redirect("/login")
        if "ID" in session:
            Key = isData(session['ID'])
            if Key:
                flash("Proszę uzupełnic wszystkie dane osobowe!")
                return redirect("/register/" + Key)
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


@app.route('/register/<string:KEY>', methods=['POST', 'GET'])
def login_data(KEY):
    if request.method == "POST":

        register_name = request.form.get('register_name', "", type=str)
        register_surname = request.form.get('register_surname', "", type=str)
        register_birth_data = request.form.get('register_birth_data', "", type=str)
        register_PESEL = request.form.get('register_PESEL', "", type=str)
        register_street = request.form.get('register_street', "", type=str)
        register_city = request.form.get('register_city', "", type=str)
        register_zip = request.form.get('register_zip', "", type=str)
        register_state = request.form.get('register_state', "", type=str)
        register_phone_number = request.form.get('register_phone_number', "", type=str)
        register_email = request.form.get('register_email', "", type=str)

        if updateUserData(session['ID'], register_name, register_surname, register_birth_data, register_PESEL, register_street, register_city, register_zip, register_state, register_phone_number):
            return jsonify({"redirect": "/"})

    return render_template("register_data.html", States=getStates())


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":

        register_mail = request.form.get('register_mail', "", type=str)
        register_password = request.form.get('register_password', "", type=str)
        register_repeat_password = request.form.get('register_repeat_password', "", type=str)

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
        if userRegister(register_mail, register_password, register_repeat_password):

            session['isLogged'] = True
            session['user'] = register_mail
            session['ID'] = getUserID(register_mail)

            return jsonify({"redirect": "/"})
        else:
            return jsonify({"title": "", "message": "Proszę wprowadzić poprawne dane!"})

    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('isLogged', None)
    session.pop('user', None)
    session.pop('ID', None)
    return redirect("/")

####################
### Company
####################

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
            flash("Firma została zarejestrowana!")
            return jsonify({"redirect": "/company/list"})

    return render_template("company_add.html", States=getStates())


@app.route('/company/list')
@app.route('/company/list/<int:ID>')
@protected
def company_list(ID=False):

    CompaniesList = getUserCompaniesList(session['ID'])

    if not ID and CompaniesList:
        ID = CompaniesList[0][0]

    if not CompaniesList:
        flash("Nie jesteś przypisany do żadnej firmy!")
        return redirect("/")

    CompaniesData = getCompanyData(ID)

    return render_template("company_list.html", SelectedID=ID, CompaniesList=CompaniesList, CompaniesData=CompaniesData)


@app.route('/company/workers', methods=['POST', 'GET'])
@app.route('/company/workers/<int:companyID>', methods=['POST', 'GET'])
@protected
def company_workers(companyID=False):

    if request.method == 'GET':
        Companies = getUserCompaniesList(session['ID'])

        if not companyID and Companies:
            companyID = Companies[0][0]

        if not Companies:
            flash("Nie jesteś przypisany do żadnej firmy!")
            return redirect("/")

        UsersData = []

        WorkersList = getCompanyWorkersID(companyID)
        PositionsList = getCompanyPositionsList(companyID)

        for WorkerID in WorkersList:

            print("ID: " + str(companyID))
            print("WorkerID: " + str(WorkerID[0]))

            # Pobieranie danych dotyczących pracownika
            UserData = getUserBasicData(WorkerID[0])
            UserCompanyData = getCompanyUserData(companyID, WorkerID[0])

            User = []

            for Data in UserData:
                User.append(Data)

            for Data in UserCompanyData:
                User.append(Data)

            # Tworznie 2D tabeli
            UsersData.append(User)
            print(UserData)

    if request.method == 'POST':

        # Dodatanie nowego pracownika
        if request.form['do'] == "add":

            if getUserPermission(session["ID"], companyID, "Add_User"):

                company_workers_name = request.form['company_workers_add_name']
                company_workers_surname = request.form['company_workers_add_surname']
                company_workers_mail = request.form['company_workers_add_mail']
                company_workers_position = request.form['company_workers_add_position']
                company_workers_salary = request.form['company_workers_add_salary']

                if addUserToCompany(company_workers_name, company_workers_surname, company_workers_mail, company_workers_position, company_workers_salary, companyID):
                    flash("Pracownik został dodany!")
                    return jsonify({"redirect": "/company/workers"})

            else:
                flash("Nie posiadasz uprawnień!")
                return jsonify({"redirect": "/company/workers"})

        # Edycja pracownika
        if request.form['do'] == "edit":

            if getUserPermission(session["ID"], companyID, "Modify_User"):

                company_workers_id = request.form['company_workers_id']
                company_workers_salary = request.form['company_workers_edit_salary']
                company_workers_position = request.form['company_workers_edit_position']

                if updateUserCompanyData(companyID, company_workers_id, company_workers_position, company_workers_salary):
                    flash("Udało sie!")
                    return jsonify({"redirect": "/company/workers"})

            else:
                flash("Nie posiadasz uprawnień!")
                return jsonify({"redirect": "/company/workers"})

    return render_template("company_workers.html", UserID=session['ID'], SelectedID=companyID, CompaniesNames=Companies, UsersData=UsersData, PositionsList=PositionsList)


@app.route('/company/workers/details')
@app.route('/company/workers/details/<int:companyID>/<int:userID>')
@protected
def company_workers_details(companyID=False, userID=False):

    Companies = getUserCompaniesList(session['ID'])

    if not userID and Companies:
        userID = Companies[0][0]

    if not Companies:
        flash("Nie jesteś przypisany do żadnej firmy!")
        return redirect("/")

    if getUserPermission(session["ID"], companyID, "View_User"):

        # Pobieranie danych dotyczących pracownika
        UserData = getUserData(userID)
        UserCompanyData = getCompanyUserData(companyID, userID)

        print(UserCompanyData)
        Netto = bruttoToNetto(UserCompanyData[2])

    else:
        flash("Nie posiadasz uprawnień!")
        return redirect("/company/workers")

    return render_template("company_workers_details.html", UserData=UserData, UserCompanyData=UserCompanyData, Netto=Netto)


@app.route('/company/workers/delete')
@app.route('/company/workers/delete/<int:companyID>/<int:userID>')
@protected
def company_workers_delete(companyID=False, userID=False):

    if getUserPermission(session["ID"], companyID, "Remove_User"):

        if userID != session['ID']:
            if deleteUserFromCompany(userID, companyID):
                flash("Pomyślnie usunięto!")
            return redirect("/company/workers")
        else:
            flash("Nie możesz usunąc samego siebie!")
            return redirect("/company/workers")

    else:
        flash("Nie posiadasz uprawnień!")
        return redirect("/company/workers")


@app.route('/company/generator')
@protected
def company_generator():
    return render_template("company_generator.html")

####################
### Vacations
####################

@app.route('/company/vacation/')
@app.route('/company/vacation/<int:companyID>')
@protected
def company_workers_vacations(companyID=False):

    Companies = getUserCompaniesList(session['ID'])

    if not companyID and Companies:
        companyID = Companies[0][0]

    if not Companies:
        flash("Nie jesteś przypisany do żadnej firmy!")
        return redirect("/")

    if getUserPermission(session["ID"], companyID, "View_Vacations"):

        Table = []

        Vacations = getCompanyVacations(companyID)
        if Vacations:
            for key, NR in enumerate(Vacations):
                BasicData = getUserBasicData(NR[1])

                Data = [Vacations[key][0], BasicData[1], BasicData[2], Vacations[key][2], Vacations[key][3],
                            Vacations[key][4], Vacations[key][5]]
                Table.append(Data)

    else:
        flash("Nie posiadasz uprawnień!")
        return redirect("/")

    return render_template("company_workers_vacations.html", SelectedID=companyID, CompaniesNames=Companies, Vacations=Table)


@app.route('/company/vacation/accept/<int:companyID>/<int:userID>')
@protected
def company_workers_vacations_accept(companyID, userID):

    if getUserPermission(session["ID"], companyID, "Accept_Vacations"):

        if acceptVacation(userID):
            flash("Urlop został zatwierdzony!")
            return redirect("/company/vacation/")

    else:
        flash("Nie posiadasz uprawnień!")
        return redirect("/company/vacation/")


@app.route('/company/vacation/cancel/<int:companyID>/<int:userID>')
@protected
def company_workers_vacations_cancel(companyID, userID):

    if getUserPermission(session["ID"], companyID, "Accept_Vacations"):

        if cancelVacation(userID):
            flash("Urlop został anulowany!")
            return redirect("/company/vacation/")

    else:

        flash("Nie posiadasz uprawnień!")
        return redirect("/company/vacation/")


@app.route('/company/vacation/add')
@protected
def company_workers_vacations_add():
    print("TEST")

####################
### Permissions
####################

@app.route('/company/permissions', methods=['POST', 'GET'])
@app.route('/company/permissions/<int:companyID>', methods=['POST', 'GET'])
@protected
def company_permissions(companyID=False):

    Companies = getUserCompaniesList(session['ID'])

    if not companyID and Companies:
        companyID = Companies[0][0]

    if not Companies:
        flash("Nie jesteś przypisany do żadnej firmy!")
        return redirect("/")

    if getUserPermission(session["ID"], companyID, "View_Position"):

        PositionsList = getCompanyPositionsList(companyID)

        PermissionsList = getCompanyPermissionsList()

    else:
        flash("Nie posiadasz uprawnień!")
        return redirect("/")

    if request.method == 'POST':

        # Dodatanie nowego pracownika
        # if request.form['do'] == "add":

        if getUserPermission(session["ID"], companyID, "Add_Position"):

            View_User = request.form["View_User"]
            Add_User = request.form["Add_User"]
            Remove_User = request.form["Remove_User"]
            Modify_User = request.form["Modify_User"]
            View_Position = request.form["View_Position"]
            Add_Position = request.form["Add_Position"]
            Remove_Position = request.form["Remove_Position"]
            View_Vacations = request.form["View_Vacations"]
            View_User = request.form["View_User"]
            print(View_User)


    return render_template("company_permissions.html", SelectedID=companyID, CompaniesNames=Companies, PositionsList=PositionsList, PermissionsList=PermissionsList)

####################
### Account
####################

@app.route('/account/')
@protected
def account():

    UserData = getUserData(session["ID"])

    return render_template("account.html", UserData=UserData)


@app.route('/account/password', methods=['POST', 'GET'])
@protected
def account_password():

    if request.method == 'POST':
        password_old = request.form['password_old']
        password_new = request.form['password_new']
        password_new_repeat = request.form['password_new_repeat']

        if password_new == password_new_repeat:
            if changePassword(session['ID'], password_old, password_new):
                flash("Hasło zostało zmienione!")
                return jsonify({"redirect": "/logout"})
            else:
                return jsonify({"title": "", "message": "Bład, sprawdz czy zostały wpisane poprawne dane!", "type": "danger"})
        else:
            return jsonify({"title": "", "message": "Hasła muszą być identyczne!", "type": "danger"})

    return render_template("account_password.html")\


@app.route('/account/edit', methods=['POST', 'GET'])
@protected
def account_edit():

    if request.method == 'POST':
        account_edit_name = request.form['account_edit_name']
        account_edit_surname = request.form['account_edit_surname']
        account_edit_birth_data = request.form['account_edit_birth_data']
        account_edit_PESEL = request.form['account_edit_PESEL']
        account_edit_street = request.form['account_edit_street']
        account_edit_city = request.form['account_edit_city']
        account_edit_zip = request.form['account_edit_zip']
        account_edit_state = request.form['account_edit_state']
        account_edit_phone_number = request.form['account_edit_phone_number']

        if updateUserData(session["ID"], account_edit_name, account_edit_surname, account_edit_birth_data, account_edit_PESEL, account_edit_street, account_edit_city, account_edit_zip, account_edit_state, account_edit_phone_number):
            print("Udalos ie")
            flash("Zaaktualizowano informacje!")
            return jsonify({"redirect": "/account"})

    return render_template("account_edit.html", States=getStates())

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

    # Blokada pisania do siebie
    if session['ID'] == ID:
        flash("Nie możesz pisać sam do siebie!")
        return redirect("/")

    IDs = getMessagesListUsersID(session['ID']) or False
    if IDs or ID:
        BasicData = getMessagesBasicData(session['ID'], IDs)
        LatestMessages = getLatestMessages(session['ID'], IDs)

        Table = []

        if IDs:
            for key, NR in enumerate(IDs):
                Data = [BasicData[key][0], BasicData[key][1], BasicData[key][2], LatestMessages[key][0],
                        LatestMessages[key][1], LatestMessages[key][2]]
                Table.append(Data)

        if ID:
            Messages = getMessages(session['ID'], ID)

            return render_template("messages.html", Table=Table, ID=session['ID'], Messages=Messages)
        else:
            return render_template("messages.html", Table=Table)
    else:
        flash("Nie posiadasz żadnych wiadomości!")
        return redirect("/")

####################
### Others
####################


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=70)

