from app import *
from others import *

from hashlib import md5


def getUserID(mail):
    if mail:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT ID FROM Users WHERE Mail = '" + str(mail) + "'")
            ID = cursor.fetchone()
            cursor.close()

            return ID[0]

        except Exception as Error:
            print("getUserID - Error")
            print("Error: " + str(Error))
    else:
        print("getUserID - Missing value")

def getCompanyName(ID):
    if ID:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT Name FROM Companies WHERE ID = '" + str(ID) + "'")
            Name = cursor.fetchone()
            cursor.close()

            return Name[0]

        except Exception as Error:
            print("getCompanyName - Error")
            print("Error: " + str(Error))
    else:
        print("getCompanyName - Missing value")

####################
### Login & Register
####################

def userLogin(login_mail, login_password):
    if login_mail and login_password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `Users` WHERE `Mail` = '" + login_mail + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `Password`, `Secret_Key` FROM `Users` WHERE `Mail` = '" + login_mail + "'")
                Data = cursor.fetchall()[0]

                # Szyfrowanie
                login_password = md5(login_password.encode('utf-8')).hexdigest()
                login_password = md5((login_password + Data[1]).encode('utf-8')).hexdigest()

                # Development
                if Type == "Development":
                    print("Hasło zaszyfrowane: " + login_password)

                # Sprawdzanie czy hasła są sobie równe
                if login_password == Data[0]:
                    return True

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("userLogin - MySQL Error")
            print("Error: " + str(Error))

def userRegister(register_mail, register_password, register_repeat_password):
    if register_mail and register_password and register_repeat_password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `Users` WHERE `Mail` = '" + register_mail + "'")
            if not cursor.fetchone()[0]:
                generatedPassword = passwordGenerator()

                # Szyfrowanie
                register_password = md5(register_password.encode('utf-8')).hexdigest()
                register_password = md5((register_password + generatedPassword).encode('utf-8')).hexdigest()

                # Dodanie do bazy MySQL
                to_MySQL = (str(register_mail), str(register_password), generatedPassword)
                cursor.execute("INSERT INTO Users (Mail, Password, Secret_Key) VALUES (%s, %s, %s)", to_MySQL)
                connection.commit()

                return True

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("registerLogin - MySQL Error")
            print("Error: " + str(Error))

####################
### Companies
####################

def companyRegister(userID, company_add_name, company_add_nip, company_add_regon, company_add_address, company_add_city,
                    company_add_code, company_add_state, company_add_phone, company_add_mail):
    if userID and company_add_name and company_add_nip and company_add_regon and company_add_address and company_add_city and company_add_code and company_add_state and company_add_phone and company_add_mail:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Tworzenie tabel
            cursor.execute("CREATE TABLE " + str(company_add_name) + '_Users'"("
                                                                     "ID INT(16) UNSIGNED PRIMARY KEY, "
                                                                     "Mail VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "Name VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "Surname VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "PESEL INT(11) NULL DEFAULT NULL, "
                                                                     "Position VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "Birth_date DATE NULL DEFAULT NULL,"
                                                                     "Phone_number VARCHAR(15) NULL DEFAULT NULL, "
                                                                     "Address VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "City VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "State VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "Code VARCHAR(6) NULL DEFAULT NULL, "
                                                                     "Salary INT(64) NULL DEFAULT NULL"
                                                                     ")")

            cursor.execute("CREATE TABLE " + str(company_add_name) + '_Permissions'"("
                                                                     "ID INT(16) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                                                                     "Name VARCHAR(128) NOT NULL, "
                                                                     "View_User BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Add_User BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Remove_User BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Modify_User BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "View_Position BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Add_Position BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Remove_Position BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Modify_Position BOOLEAN NOT NULL DEFAULT FALSE "
                                                                     ")")

            cursor.execute("CREATE TABLE " + str(company_add_name) + '_Messages'"("
                                                                     "ID INT(16) UNSIGNED AUTO_INCREMENT PRIMARY KEY, "
                                                                     "Sender_ID INT(16) NOT NULL, "
                                                                     "Recipient_ID INT(16) NOT NULL, "
                                                                     "Message TEXT NOT NULL, "
                                                                     "Time TIMESTAMP NOT NULL "
                                                                     ")")

            # Pobranie State po ID
            cursor.execute("SELECT Name FROM States WHERE ID = '" + str(company_add_state) + "'")
            State = cursor.fetchone()[0]

            # Dodanie do bazy "Companies"
            to_MySQL = (str(company_add_name), int(company_add_nip), int(company_add_regon), str(company_add_address),
                        str(company_add_city), str(State), str(company_add_code), str(company_add_phone),
                        str(company_add_mail))
            cursor.execute(
                "INSERT INTO Companies (Name, NIP, REGON, Address, City, State, Code, Phone, Mail) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                to_MySQL)
            connection.commit()

            # Pobranie ID firmy
            cursor.execute("SELECT ID FROM Companies ORDER BY ID DESC LIMIT 1")
            ID = cursor.fetchone()[0]

            # Dodanie do bazy "Companies_Workers"
            to_MySQL = (userID, str(company_add_name), ID)
            cursor.execute("INSERT INTO Companies_Workers (User_ID, Company_Name, Company_ID) VALUES (%s, %s, %s)",
                           to_MySQL)
            connection.commit()

            # Pobranie Mail'a
            cursor.execute("SELECT Mail FROM Users WHERE ID = '" + str(userID) + "'")
            userMail = cursor.fetchone()[0]

            # Dodanie do bazy "_Permissions"
            to_MySQL = ("Owner", True, True, True, True, True, True, True, True)
            cursor.execute("INSERT INTO " + str(
                company_add_name) + '_Permissions'" (Name, View_User, Add_User, Remove_User, Modify_User, View_Position, Add_Position, Remove_Position, Modify_Position) VALUES (%s, %r, %r, %r, %r, %r, %r, %r, %r)",
                           to_MySQL)
            connection.commit()

            # Dodanie do bazy "_Users"
            to_MySQL = (userID, userMail, "Owner")
            cursor.execute("INSERT INTO " + str(company_add_name) + '_Users'" (ID, Mail, Position) VALUES (%s, %s, %s)",
                           to_MySQL)
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            return True

        # Error Log
        except Exception as Error:
            print("companyRegister - MySQL Error")
            print("Error: " + str(Error))

def checkCompany(company_add_name, company_add_nip, company_add_regon):
    # Łączność z MYSQL
    connection = mysql.connect()
    cursor = connection.cursor()

    # Sprawdzanie czy istnieje FIRMA
    cursor.execute("SELECT COUNT(1) FROM `Companies` WHERE `Name` = '" + company_add_name + "'")
    if cursor.fetchone()[0]:
        return True

    # Sprawdzanie czy istnieje NIP lub Regon
    cursor.execute("SELECT COUNT(1) FROM `Companies` WHERE `NIP` = '" + company_add_nip + "'")
    if cursor.fetchone()[0]:
        return True

    cursor.execute("SELECT COUNT(1) FROM `Companies` WHERE `REGON` = '" + company_add_regon + "'")
    if cursor.fetchone()[0]:
        return True

def getUserCompaniesList(userID):
    if userID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute(
                "SELECT Company_ID, Company_Name FROM Companies_Workers WHERE `User_ID` = '" + str(userID) + "'")
            Companies = cursor.fetchall()

            # Development
            if Type == "Development":
                print("getUserCompaniesList: " + str(Companies))

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Wartość zwrotna
            return Companies

        # Error Log
        except Exception as Error:
            print("getUserCompaniesList - MySQL Error")
            print("Error: " + str(Error))

def getCompanyData(companyID):
    if companyID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT Name, NIP, REGON, Address, City, State, Code, Phone, Mail FROM Companies WHERE ID = '" + str(
                companyID) + "'")
            Companies = cursor.fetchone()

            # Development
            if Type == "Development":
                print("getCompanyData: " + str(Companies))

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Rozłączenie z bazą MySQL
            return Companies

        # Error Log
        except Exception as Error:
            print("getCompanyData - MySQL Error")
            print("Error: " + str(Error))


####################
### Others
####################

def getStates():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT `ID`, `Name` FROM States")
        States = cursor.fetchall()
        cursor.close()

        return States

    except Exception as Error:
        print("getStates - Error")
        print("Error: " + str(Error))
