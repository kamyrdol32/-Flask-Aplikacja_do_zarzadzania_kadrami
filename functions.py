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
                login_password = md5((login_password+Data[1]).encode('utf-8')).hexdigest()

                # Development
                if Type == "Development":
                    print(Data[0])
                    print(Data[1])
                    print(login_password)

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
                register_password = md5((register_password+generatedPassword).encode('utf-8')).hexdigest()

                # Dodanie do bazy MySQL
                to_MySQL = (str(register_mail), str(register_password), generatedPassword, 1, 1)
                cursor.execute("INSERT INTO Users (Mail, Password, Secret_Key, Type, Status) VALUES (%s, %s, %s, %s, %s)", to_MySQL)
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

def companyRegister(userID, company_add_name, company_add_nip, company_add_regon, company_add_street, company_add_city, company_add_zip, company_add_state):
    if userID and company_add_name and company_add_nip and company_add_regon and company_add_street and company_add_city and company_add_zip and company_add_state:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Dodanie do bazy MySQL
            to_MySQL = (str(company_add_name), int(userID))
            cursor.execute("INSERT INTO Companies (Company_Name, Owner_ID) VALUES (%s, %s)", to_MySQL)
            connection.commit()

            cursor.execute("SELECT ID FROM Companies WHERE Company_Name = '" + str(company_add_name) + "'")
            ID = cursor.fetchone()[0]

            to_MySQL = (ID, company_add_name, company_add_nip, company_add_regon, company_add_state, company_add_city, company_add_street, company_add_zip)
            cursor.execute("INSERT INTO Companies_Data (Company_ID, Name, NIP, Regon, State, City, Street, Code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", to_MySQL)
            connection.commit()

            return True

            # Rozłączenie z bazą MySQL
            cursor.close()

            print("1")

        # Error Log
        except Exception as Error:
            print("registerLogin - MySQL Error")
            print("Error: " + str(Error))


def checkCompany(company_add_nip, company_add_regon):

    # Łączność z MYSQL
    connection = mysql.connect()
    cursor = connection.cursor()

    # Sprawdzanie czy istnieje NIP lub Regon
    cursor.execute("SELECT COUNT(1) FROM `Companies_Data` WHERE `NIP` = '" + company_add_nip + "'")
    if cursor.fetchone()[0]:
        return True

    cursor.execute("SELECT COUNT(1) FROM `Companies_Data` WHERE `Regon` = '" + company_add_regon + "'")
    if cursor.fetchone()[0]:
        return True

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
