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

                # Pobieranie hasła
                cursor.execute("SELECT `password`, `secret` FROM `user` WHERE `email` = '" + email + "'")
                db = cursor.fetchall()[0]
                password = md5(password.encode('utf-8')).hexdigest()
                password = md5((password+db[1]).encode('utf-8')).hexdigest()

                print(db[0])
                print(db[1])
                print(password)
                # Sprawdzanie czy hasła są sobie równe
                if password == db[0]:
                    flash('Pomyślnie zalogowano!', 'success')
                    return True
                else:
                    flash('Proszę wprowadzić poprawne dane!', 'danger')
            else:
                flash('Podany E-Mail nie istnieje w naszej bazie!', 'danger')
            cursor.close()
        except Exception as Error:
            print("userLogin - MySQL Error")
            print("Error: " + str(Error))
    else:
        print("Prosze wprowadzić login oraz hasło!")
