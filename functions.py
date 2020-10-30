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
            cursor.execute("SELECT COUNT(1) FROM Users WHERE Mail = '" + email + "'")
            if cursor.fetchone()[0]:

                # Pobieranie hasła
                cursor.execute("SELECT Password FROM Users WHERE Mail = '" + email + "'")
                mysql_password = cursor.fetchone()[0]

                # Sprawdzanie czy hasła są sobie równe
                if md5(password.encode('utf-8')).hexdigest() == mysql_password:
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