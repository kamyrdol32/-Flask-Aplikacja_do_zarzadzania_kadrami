from app import *
from others import *

from hashlib import md5

####################
### Login & Register
####################

def userLogin(login_email, login_password):
    if login_email and login_password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `user` WHERE `email` = '" + login_email + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `password`, `secret` FROM `user` WHERE `email` = '" + login_email + "'")
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
            cursor.execute("SELECT COUNT(1) FROM `user` WHERE `email` = '" + register_mail + "'")
            if not cursor.fetchone()[0]:

                # Dodanie do bazy MySQL
                to_MySQL = (str(register_mail), str(register_password), passwordGenerator(), 1, 1)
                print(to_MySQL)
                cursor.execute("INSERT INTO user (email, password, secret, type, status) VALUES (%s, %s, %s, %s, %s)", to_MySQL)
                connection.commit()

                return True

            # Rozłączenie z bazą MySQL
            cursor.close()

        # Error Log
        except Exception as Error:
            print("registerLogin - MySQL Error")
            print("Error: " + str(Error))