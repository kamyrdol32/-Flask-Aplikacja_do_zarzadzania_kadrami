from app import *
from hashlib import md5

####################
### Login & Register
####################

def userLogin(email, password):
    if email and password:
        try:
            # Łączność z MYSQL
            connection = mysql.connect()
            cursor = connection.cursor()

            # Sprawdzanie czy istnieje użytkownik
            cursor.execute("SELECT COUNT(1) FROM `user` WHERE `email` = '" + email + "'")
            if cursor.fetchone()[0]:

                # Pobieranie danych
                cursor.execute("SELECT `password`, `secret` FROM `user` WHERE `email` = '" + email + "'")
                Data = cursor.fetchall()[0]

                # Szyfrowanie
                password = md5(password.encode('utf-8')).hexdigest()
                password = md5((password+Data[1]).encode('utf-8')).hexdigest()

                # Development
                if Type == "Development":
                    print(Data[0])
                    print(Data[1])
                    print(password)

                # Sprawdzanie czy hasła są sobie równe
                if password == Data[0]:
                    return True

            cursor.close()

        # Error Log
        except Exception as Error:
            print("userLogin - MySQL Error")
            print("Error: " + str(Error))


def userRegister()