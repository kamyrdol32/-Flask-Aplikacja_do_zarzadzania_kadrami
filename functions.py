from app import *
from others import *
import xlsxwriter

from hashlib import md5


def getUserID(mail):
    if mail:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT ID FROM Authorization WHERE Mail = '" + str(mail) + "'")
            ID = cursor.fetchone()
            cursor.close()

            return ID[0]

        except Exception as Error:
            print("getUserID - Error")
            print("Error: " + str(Error))
    else:
        print("getUserID - Missing value")

def getUserData(ID):
    if ID:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE ID = '" + str(ID) + "'")
            UserData = cursor.fetchone()
            cursor.close()

            # Development
            if Type == "Development":
                print("getUserData: " + str(UserData))

            return UserData

        except Exception as Error:
            print("getUserData - Error")
            print("Error: " + str(Error))
    else:
        print("getUserData - Missing value")

def getUserBasicData(ID):
    if ID:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT ID, Name, Surname, Phone_number FROM Users WHERE ID = '" + str(ID) + "'")
            UserData = cursor.fetchone()
            cursor.close()

            # Development
            if Type == "Development":
                print("getUserBasicData: " + str(UserData))

            return UserData

        except Exception as Error:
            print("getUserBasicData - Error")
            print("Error: " + str(Error))
    else:
        print("getUserBasicData - Missing value")

def getCompanyUserData(companyID, userID):
    if companyID and userID:
        try:
            companyName = getCompanyName(companyID)

            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM " + str(companyName) + '_Users'" WHERE ID = '" + str(userID) + "'")
            UserData = cursor.fetchone()
            cursor.close()

            # Development
            if Type == "Development":
                print("getCompanyUserData: " + str(UserData))

            return UserData

        except Exception as Error:
            print("getCompanyUserData - Error")
            print("Error: " + str(Error))
    else:
        print("getCompanyUserData - Missing value")

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
            cursor.execute("SELECT COUNT(1) FROM `Authorization` WHERE `Mail` = '" + login_mail + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `Password`, `Secret_Key` FROM `Authorization` WHERE `Mail` = '" + login_mail + "'")
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
            cursor.execute("SELECT COUNT(1) FROM `Authorization` WHERE `Mail` = '" + register_mail + "'")
            if not cursor.fetchone()[0]:
                generatedPassword = passwordGenerator()

                # Szyfrowanie
                register_password = md5(register_password.encode('utf-8')).hexdigest()
                register_password = md5((register_password + generatedPassword).encode('utf-8')).hexdigest()

                # Dodanie do bazy MySQL
                to_MySQL = (str(register_mail), str(register_password), generatedPassword)
                cursor.execute("INSERT INTO Authorization (Mail, Password, Secret_Key) VALUES (%s, %s, %s)", to_MySQL)
                connection.commit()

                ID = getUserID(str(register_mail))

                # Dodanie do bazy MySQL
                to_MySQL = (ID, str(register_mail))
                cursor.execute("INSERT INTO Users (ID, Mail) VALUES (%s, %s)", to_MySQL)
                connection.commit()

                return True

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("registerLogin - MySQL Error")
            print("Error: " + str(Error))

def isData(ID):
    if ID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT Name, Surname, PESEL, Birth_date, Phone_number, Address, City, State, Code FROM Users WHERE ID = '" + str(ID) + "'")
            Data = cursor.fetchone()

            cursor.execute("SELECT Secret_Key FROM Authorization WHERE ID = '" + str(ID) + "'")
            Key = cursor.fetchone()[0]

            # Development
            if Type == "Development":
                print("isData: " + str(Data))
                print("isData Key: " + str(Key))

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Return
            if Data[0] and Data[1] and Data[2] and Data[3] and Data[4] and Data[5] and Data[6] and Data[7] and Data[8]:
                return False
            else:
                return Key

        # Error Log
        except Exception as Error:
            print("isData - MySQL Error")
            print("Error: " + str(Error))

def updateUserData(ID, register_name, register_surname, register_birth_data, register_PESEL, register_street, register_city, register_zip, register_state, register_phone_number):
    if ID and register_name and register_surname and register_birth_data and register_PESEL and register_street and register_city and register_zip and register_state and register_phone_number:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Pobranie State po ID
            cursor.execute("SELECT Name FROM States WHERE ID = '" + str(register_state) + "'")
            State = cursor.fetchone()[0]

            cursor.execute("UPDATE Users SET Name = '" + str(register_name) + "', Surname = '" + str(register_surname) + "', PESEL = '" + str(register_PESEL) + "', Birth_date = '" + str(register_birth_data) + "', Phone_number = '" + str(register_phone_number) + "', Address = '" + str(register_street) + "', City = '" + str(register_city) + "', State = '" + str(State) + "', Code = '" + str(register_zip) + "' WHERE `ID` = '" + str(ID) + "'")
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            return True

        # Error Log
        except Exception as Error:
            print("updateUserData - MySQL Error")
            print("Error: " + str(Error))

def changePassword(userID, password_old, password_new):
    if userID and password_old and password_new:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Pobieranie danych
            cursor.execute("SELECT `Password`, `Secret_Key` FROM `Authorization` WHERE `ID` = '" + str(userID) + "'")
            Data = cursor.fetchall()[0]

            # Szyfrowanie
            password_old = md5(password_old.encode('utf-8')).hexdigest()
            password_old = md5((password_old + Data[1]).encode('utf-8')).hexdigest()

            # Development
            if Type == "Development":
                print("Stare hasło zaszyfrowane: " + password_old)

            # Sprawdzanie czy hasła są sobie równe
            if password_old == Data[0]:

                generatedPassword = passwordGenerator()

                # Szyfrowanie
                password_new = md5(password_new.encode('utf-8')).hexdigest()
                password_new = md5((password_new + generatedPassword).encode('utf-8')).hexdigest()

                # Development
                if Type == "Development":
                    print("Nowe hasło zaszyfrowane: " + password_new)

                cursor.execute("UPDATE Authorization SET Password = '" + str(password_new) + "', Secret_Key = '" + str(generatedPassword) + "' WHERE `ID` = '" + str(userID) + "'")
                connection.commit()

                # Rozłączenie z bazą MySQL
                cursor.close()

                return True

            else:
                # Rozłączenie z bazą MySQL
                cursor.close()

                return False

        # Error Log
        except Exception as Error:
            print("updateUserData - MySQL Error")
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
                                                                     "Position VARCHAR(128) NULL DEFAULT NULL, "
                                                                     "Salary BIGINT(64) NULL DEFAULT NULL,"
                                                                     "Registered DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP"
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
                                                                     "Modify_Position BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "View_Vacations BOOLEAN NOT NULL DEFAULT FALSE, "
                                                                     "Accept_Vacations BOOLEAN NOT NULL DEFAULT FALSE "
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

            # # Pobranie Mail'a
            # cursor.execute("SELECT Mail FROM Authorization WHERE ID = '" + str(userID) + "'")
            # userMail = cursor.fetchone()[0]

            # Dodanie do bazy "_Permissions"
            to_MySQL = ("Owner", True, True, True, True, True, True, True, True, True, True)
            cursor.execute("INSERT INTO " + str(
                company_add_name) + '_Permissions'" (Name, View_User, Add_User, Remove_User, Modify_User, View_Position, Add_Position, Remove_Position, Modify_Position, View_Vacations, Accept_Vacations) VALUES (%s, %r, %r, %r, %r, %r, %r, %r, %r, %r, %r)",
                           to_MySQL)
            connection.commit()

            to_MySQL = ("Pracownik", False, False, False, False, False, False, False, False)
            cursor.execute("INSERT INTO " + str(
                company_add_name) + '_Permissions'" (Name, View_User, Add_User, Remove_User, Modify_User, View_Position, Add_Position, Remove_Position, Modify_Position) VALUES (%s, %r, %r, %r, %r, %r, %r, %r, %r)",
                           to_MySQL)
            connection.commit()

            # Dodanie do bazy "_Users"
            to_MySQL = (userID, "Owner")
            cursor.execute("INSERT INTO " + str(company_add_name) + '_Users'" (ID, Position) VALUES (%s, %s)",
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

def getCompanyWorkersID(companyID):
    if companyID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT User_ID FROM Companies_Workers WHERE Company_ID = '" + str(companyID) + "' ORDER BY User_ID")
            WorkersList = cursor.fetchall()

            # Development
            if Type == "Development":
                print("getCompanyWorkersID: " + str(WorkersList))

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Rozłączenie z bazą MySQL
            return WorkersList

        # Error Log
        except Exception as Error:
            print("getCompanyWorkersID - MySQL Error")
            print("Error: " + str(Error))

def addUserToCompany(name, surname, userMail, position, salary, companyID):
    if userMail and companyID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Pobieranie nazwy stanowiska
            cursor.execute("SELECT `Name` FROM " + str(getCompanyName(companyID)) + '_Permissions'" WHERE `ID` = '" + str(position) + "'")
            position = cursor.fetchone()[0]

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `Authorization` WHERE `Mail` = '" + userMail + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `ID` FROM `Authorization` WHERE `Mail` = '" + userMail + "'")
                userID = cursor.fetchone()[0]

                # Sprawdzanie czy istnieje użytkownik
                cursor.execute("SELECT COUNT(1) FROM `Companies_Workers` WHERE `User_ID` = '" + str(userID) + "' AND `Company_ID` = '" + str(companyID) + "'")
                if not cursor.fetchone()[0]:

                    # Przypisywanie do firmy
                    to_MySQL = (str(userID), str(getCompanyName(companyID)), str(companyID))
                    cursor.execute("INSERT INTO Companies_Workers (User_ID, Company_Name, Company_ID) VALUES (%s, %s, %s)", to_MySQL)
                    connection.commit()

                    to_MySQL = (str(userID), str(position), str(salary))
                    cursor.execute("INSERT INTO " + str(getCompanyName(companyID)) + '_Users'" (ID, Position, Salary) VALUES (%s, %s, %s)",
                                   to_MySQL)
                    connection.commit()

            # Brak konta
            else:
                Password = passwordGenerator()

                userRegister(userMail, Password, Password)
                sendWelcomeMail(userMail, Password, getCompanyName(companyID))

                userID = getUserID(userMail)

                # Przypisywanie do firmy
                to_MySQL = (str(userID), str(getCompanyName(companyID)), str(companyID))
                cursor.execute("INSERT INTO Companies_Workers (User_ID, Company_Name, Company_ID) VALUES (%s, %s, %s)",
                               to_MySQL)
                connection.commit()

                # Wpisanie Imie & Nazwisko
                cursor.execute("UPDATE Users SET Name = '" + str(name) + "', Surname = '" + str(surname) + "' WHERE Mail = '" + str(userMail) + "'")
                connection.commit()

                to_MySQL = (str(userID), str(position), str(salary))
                cursor.execute("INSERT INTO " + str(getCompanyName(companyID)) + '_Users'" (ID, Position, Salary) VALUES (%s, %s, %s)",
                               to_MySQL)
                connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            return True

        # Error Log
        except Exception as Error:
            print("addUserToCompany - MySQL Error")
            print("Error: " + str(Error))

def deleteUserFromCompany(userID, companyID):
    if userID and companyID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Usuwanie z MySQL
            cursor.execute("DELETE FROM Companies_Workers WHERE  User_ID = '" + str(userID) + "' AND  Company_ID = '" + str(companyID) + "'")
            connection.commit()

            cursor.execute("DELETE FROM " + str(getCompanyName(companyID)) + '_Users'" WHERE  ID = '" + str(userID) + "'")
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            return True

            # Error Log
        except Exception as Error:
            print("deleteUserFromCompany - MySQL Error")
            print("Error: " + str(Error))

def updateUserCompanyData(companyID, userID, position, salary):
    if companyID and userID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT Name FROM " + str(getCompanyName(companyID)) + '_Permissions'" WHERE ID = '" + str(position) + "'")
            position = cursor.fetchone()[0]

            cursor.execute("UPDATE " + str(getCompanyName(companyID)) + '_Users'" SET Position = '" + str(position) + "', Salary = '" + str(salary) + "' WHERE `ID` = '" + str(userID) + "'")
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            return True

        # Error Log
        except Exception as Error:
            print("updateUserCompanyData - MySQL Error")
            print("Error: " + str(Error))

####################
### Vacations
####################

def getCompanyVacations(companyID):
    if companyID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT ID, User_ID, Reason, Start_Data, End_Data, Accepted FROM Vacations WHERE Company_ID = '" + str(companyID) + "' ORDER BY ID")
            Vacations = cursor.fetchall()

            # Development
            if Type == "Development":
                print("getCompanyVacations: " + str(Vacations))

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Rozłączenie z bazą MySQL
            return Vacations

        # Error Log
        except Exception as Error:
            print("getCompanyVacations - MySQL Error")
            print("Error: " + str(Error))

def acceptVacation(vacationID):
    if vacationID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("UPDATE Vacations SET Accepted = 'Accepted' WHERE `ID` = '" + str(vacationID) + "'")
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Return
            return True

        # Error Log
        except Exception as Error:
            print("acceptVacation - MySQL Error")
            print("Error: " + str(Error))

def cancelVacation(vacationID):
    if vacationID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("UPDATE Vacations SET Accepted = 'Canceled' WHERE `ID` = '" + str(vacationID) + "'")
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Return
            return True

        # Error Log
        except Exception as Error:
            print("cancelVacation - MySQL Error")
            print("Error: " + str(Error))

def addVacation(userID, companyID, reason, start, end):
    if userID and companyID and reason and start and end:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje juz stanowisko
            cursor.execute("SELECT COUNT(1) FROM Vacations WHERE `User_ID` = '" + str(userID) + "'")
            if not cursor.fetchone()[0]:

                to_MySQL = (str(userID), str(companyID), str(reason), start, end)
                cursor.execute("INSERT INTO Vacations (User_ID, Company_ID, Reason, Start_Data, End_Data) VALUES (%s, %s, %s, %s, %s)", to_MySQL)
                connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Rozłączenie z bazą MySQL
            return True

        # Error Log
        except Exception as Error:
            print("addVacation - MySQL Error")
            print("Error: " + str(Error))

####################
### Permissions
####################

def getUserPermission(userID, companyID, permission):
    if userID and companyID and permission:
        try:
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT Position FROM " + str(getCompanyName(companyID)) + '_Users'" WHERE ID = '" + str(userID) + "'")
            Position = cursor.fetchone()

            cursor.execute("SELECT " + str(permission) + " FROM " + str(getCompanyName(companyID)) + '_Permissions'" WHERE Name = '" + str(Position[0]) + "'")
            Permission = cursor.fetchone()
            cursor.close()

            # Development
            if Type == "Development":
                print("getUserPermission: " + str(permission))
                print("getUserPermission: " + str(Permission[0]))

            return Permission[0]

        except Exception as Error:
            print("getUserPermission - Error")
            print("Error: " + str(Error))
    else:
        print("getUserPermission - Missing value")

def getCompanyPositionsList(companyID):
    if companyID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            companyName = getCompanyName(companyID)

            cursor.execute("SELECT ID, Name FROM " + str(companyName) + '_Permissions'"")
            Positions = cursor.fetchall()

            # Development
            if Type == "Development":
                print("getCompanyPositionsList: " + str(Positions))

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Rozłączenie z bazą MySQL
            return Positions

        # Error Log
        except Exception as Error:
            print("getCompanyPositionsList - MySQL Error")
            print("Error: " + str(Error))

def getCompanyPermissionsList():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        cursor.execute("SELECT `ID`, `Name`, `Description` FROM Permissions")
        States = cursor.fetchall()
        cursor.close()

        return States

    except Exception as Error:
        print("getCompanyPermissionsList - Error")
        print("Error: " + str(Error))

def addRole(companyID, Name, View_User, Add_User, Remove_User, Modify_User, View_Position, Add_Position, Remove_Position, Modify_Position, View_Vacations, Accept_Vacations):
    if companyID and Name and View_User and Add_User and Remove_User and Modify_User and View_Position and Add_Position and Remove_Position and Modify_Position and View_Vacations and Accept_Vacations:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje juz stanowisko
            cursor.execute("SELECT COUNT(1) FROM " + str(getCompanyName(companyID)) + '_Permissions'" WHERE `Name` = '" + Name + "'")
            if not cursor.fetchone()[0]:

                # # Dodanie do MySQL
                to_MySQL = (str(Name), View_User, Add_User, Remove_User, Modify_User, View_Position, Add_Position, Remove_Position, Modify_Position, View_Vacations, Accept_Vacations)
                cursor.execute("INSERT INTO " + str(getCompanyName(companyID)) + '_Permissions'" (Name, View_User, Add_User, Remove_User, Modify_User, View_Position, Add_Position, Remove_Position, Modify_Position, View_Vacations, Accept_Vacations) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", to_MySQL)
                connection.commit()

            else:

                return False

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Return
            return True

        # Error Log
        except Exception as Error:
            print("addRole - MySQL Error")
            print("Error: " + str(Error))

####################
### Messages
####################

def getMessagesListUsersID(userID):
    if userID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT Recipient_ID, Sender_ID FROM Messages WHERE Recipient_ID = '" + str(userID) + "' OR Sender_ID = '" + str(userID) + "' GROUP BY Recipient_ID")
            MessagesList = cursor.fetchall()

            # cursor.execute("SELECT * FROM Messages WHERE Recipient_ID = '" + str(userID) + "' OR Sender_ID = '" + str(userID) + "' GROUP BY Sender_ID ORDER BY ID DESC")
            # MessagesList2 = cursor.fetchall()
            # MessagesList.append(MessagesList2)

            # Rozłączenie z bazą MySQL
            cursor.close()

            Data = []

            # Tworzenie tabeli
            for X in MessagesList:
                Data.append(X[0])
                Data.append(X[1])

            # Usuwanie duplikatow & Usuwanie własnego ID
            Data = list(dict.fromkeys(Data))
            Data.remove(userID)

            # Development
            if Type == "Development":
                print("getMessagesListUsersID: " + str(Data))

            return Data

        # Error Log
        except Exception as Error:
            print("getMessagesListUsersID - MySQL Error")
            print("Error: " + str(Error))

def getMessagesBasicData(UserID, OthersIDs):
    if UserID and OthersIDs:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            Table = []

            for ID in OthersIDs:
                cursor.execute("SELECT ID, Name, Surname FROM Users WHERE ID = '" + str(ID) + "'")
                UserData = cursor.fetchone()

                Data = [UserData[0], UserData[1], UserData[2]]

                Table.append(Data)

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Development
            if Type == "Development":
                print("getMessagesBasicData: " + str(Table))

            return Table

        # Error Log
        except Exception as Error:
            print("getMessagesBasicData - MySQL Error")
            print("Error: " + str(Error))

def getLatestMessages(UserID, OthersIDs):
    if UserID and OthersIDs:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            Table = []

            for OtherID in OthersIDs:

                Data = []

                cursor.execute("SELECT Message, CAST(Time AS DATE), CAST(Time AS TIME) FROM Messages WHERE (Sender_ID = '" + str(UserID) + "' AND Recipient_ID = '" + str(OtherID) + "') OR (Sender_ID = '" + str(OtherID) + "' AND Recipient_ID = '" + str(UserID) + "') ORDER BY Time DESC LIMIT 1")
                Message = cursor.fetchone()
                Data.append(Message[0])
                Data.append(Message[1])
                Data.append(Message[2])

                Table.append(Data)

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Development
            if Type == "Development":
                print("getLatestMessages: " + str(Table))

            return Table

        # Error Log
        except Exception as Error:
            print("getLatestMessages - MySQL Error")
            print("Error: " + str(Error))

def getMessages(UserID, OtherID):
    if UserID and OtherID:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            cursor.execute("SELECT ID, Sender_ID, Recipient_ID, Message, CAST(Time AS DATE), CAST(Time AS TIME), Seen FROM Messages WHERE (Sender_ID = '" + str(UserID) + "' AND Recipient_ID = '" + str(OtherID) + "') OR (Sender_ID = '" + str(OtherID) + "' AND Recipient_ID = '" + str(UserID) + "') ORDER BY Time")
            Messages = cursor.fetchall()

            cursor.execute("UPDATE Messages SET Seen = 1 WHERE Recipient_ID = '" + str(UserID) + "' AND Sender_ID = '" + str(OtherID) + "'") # UPDATE Messages SET Seen = 1 WHERE Recipient_ID = 1 AND Sender_ID = 2
            connection.commit()

            # Rozłączenie z bazą MySQL
            cursor.close()

            # Development
            if Type == "Development":
                print("getMessages: " + str(Messages))

            return Messages

        # Error Log
        except Exception as Error:
            print("getMessages - MySQL Error")
            print("Error: " + str(Error))

def sendMessage(UserID, OtherID, Message):
    if UserID and OtherID and Message:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Dodanie do bazy MySQL
            to_MySQL = (str(UserID), str(OtherID), str(Message))
            cursor.execute("INSERT INTO Messages (Sender_ID, Recipient_ID, Message) VALUES (%s, %s, %s)", to_MySQL)
            connection.commit()

            # UPDATE Messages SET Seen = 1 WHERE Recipient_ID = 1

            # Development
            if Type == "Development":
                print("sendMessage: " + str(Message))

            # Rozłączenie z bazą MySQL
            cursor.close()

            return True

        # Error Log
        except Exception as Error:
            print("sendMessage - MySQL Error")
            print("Error: " + str(Error))

####################
### Others
####################

def bruttoToNetto(salary):
    try:
        netto = float(salary / 1.23)
        netto = round(netto, 2)

        # Development
        if Type == "Development":
            print("bruttoToNetto: " + str(netto))

        return netto

    # Error Log
    except Exception as Error:
        print("bruttoToNetto - MySQL Error")
        print("Error: " + str(Error))

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

def createExcelWorkers(companyID):
    if companyID:
        try:
            workbook = xlsxwriter.Workbook('./upload/Workers.xlsx')
            worksheet = workbook.add_worksheet()

            connection = mysql.connect()
            cursor = connection.cursor()

            companyName = getCompanyName(companyID)

            cursor.execute("SELECT * FROM Users")
            Positions = cursor.fetchall()

            # Miejsce startu
            row = 0
            col = 0

            Names = [
                "ID",
                "Mail",
                "Name ",
                "Surname",
                "PESEL",
                "Birth_date",
                "Phone_number",
                "Address",
                "City",
                "State",
                "Code"
            ]

            cursor.close()

            # Tworzenie opisow
            for Name in Names:
                worksheet.write(row, col, Name)
                col += 1

            row = 1
            col = 0

            # Wprowadzanie danych
            for Position in Positions:
                for Data in Position:
                    worksheet.write(row, col, Data)
                    col += 1
                row += 1
                col = 0

            workbook.close()

        except Exception as Error:
            print("createExcelWorkers - Error")
            print("Error: " + str(Error))

def createExcelPermissions(companyID):
    if companyID:
        try:
            workbook = xlsxwriter.Workbook('./upload/Permissions.xlsx')
            worksheet = workbook.add_worksheet()

            connection = mysql.connect()
            cursor = connection.cursor()

            companyName = getCompanyName(companyID)

            cursor.execute("SELECT * " + str(companyName) + '_Permissions'"")
            Positions = cursor.fetchall()

            # Miejsce startu
            row = 0
            col = 0

            Names = [
                "ID",
                "Name",
                "View_User ",
                "Add_User",
                "Remove_User",
                "Modify_User",
                "View_Position",
                "Add_Position",
                "Remove_Position",
                "Modify_Position",
                "View_Vacations",
                "Accept_Vacations"
            ]

            cursor.close()

            # Tworzenie opisow
            for Name in Names:
                worksheet.write(row, col, Name)
                col += 1

            row = 1
            col = 0

            # Wprowadzanie danych
            for Position in Positions:
                for Data in Position:
                    worksheet.write(row, col, Data)
                    col += 1
                row += 1
                col = 0

            workbook.close()

        except Exception as Error:
            print("createExcelPermissions - Error")
            print("Error: " + str(Error))