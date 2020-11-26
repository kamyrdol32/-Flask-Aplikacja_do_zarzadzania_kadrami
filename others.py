from app import *

import random
import string
import re

from flask_mail import Message

def sendWelcomeMail(recipient, password, companyName):
    msg = Message('Aplikacja do zarzadzania kadrami', sender='kamyrdol32test@gmail.com', recipients=[recipient])
    msg.html = "<h3>Witaj " + recipient + "</h3><br>Zostałeś zarejestrowany w firmie " + companyName + ", witamy na pokładzie!<br>Mamy nadzieję, że Ci sie tu spodoba.<br><br>Poniżej przekazujemy Ci Twoje prywatne hasło do przeprowadzenia procesu pierwszego logowania.<br><br><b>Login:</b> " + recipient + "<br><b>Hasło:</b> " + password + "<br><br>Rekomendujemy natychmiastową zmianę hasła po logowaniu.<br><b>Bezpieczeństwo przede wszystkim!</b><br><br>Zapraszamy<br>http://evgaming.duckdns.org:70/"
    mail.send(msg)

def passwordGenerator(stringlength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringlength))


# Weryfikacja danych
# if not check("String", register_name):
#     return jsonify({"title": "", "message": "Prosze wprowadzić poprawne Imię!"})
# if not check("String", register_surname):
#     return jsonify({"title": "", "message": "Prosze wprowadzić poprawne Nazwisko!"})
# if not check("Birth_Data", register_birth_data):
#     return jsonify({"title": "", "message": "Prosze wprowadzić poprawną Datę urodzenia!"})
# if not check("PESEL", register_PESEL):
#     return jsonify({"title": "", "message": "Prosze wprowadzić poprawny PESEL!"})
# if not check("String", register_city):
#     return jsonify({"title": "", "message": "Prosze wprowadzić poprawne Miasto!"})
# if not check("Phone_Number", register_phone_number):
#     return jsonify({"title": "", "message": "Prosze wprowadzić poprawny Numer Telefonu!"})


Regex_Mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
Regex_String = '[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż]$'
Regex_Birth_Data = '^([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))$'
Regex_PESEL = '(\d{11})$'
Regex_NIP = '(\d{10})$'
Regex_REGON = '(\d{9})$'
Regex_Phone_Number = '(\d{9})$'

def check(Type, Object):
    print(Type + " " + Object)
    if Type == "Mail":
        if re.search(Regex_Mail, Object) or Object == "admin":
            return True
        else:
            return False
    elif Type == "Phone_Number":
        if len(Object) == 9:
            return True
        else:
            return False
    elif Type == "String":
        if re.search(Regex_String, Object) and Object != "":
            return True
        else:
            return False
    elif Type == "Name":
        if re.search(Regex_String, Object) and not (' ' in Object) and Object != "":
            return True
        else:
            return False
    elif Type == "Birth_Data":
        if re.search(Regex_Birth_Data, Object) and Object != "":
            return True
        else:
            return False
    elif Type == "PESEL":
        if re.search(Regex_PESEL, Object) and Object != "" and len(Object) == 11:
            return True
        else:
            return False
    elif Type == "Phone_Number":
        if re.search(Regex_Phone_Number, Object) and Object != "" and len(Object) == 9:
            return True
        else:
            return False
    elif Type == "NIP":
        if re.search(Regex_NIP, Object) and Object != "" and len(Object) == 10:
            return True
        else:
            return False
    elif Type == "REGON":
        if re.search(Regex_REGON, Object) and Object != "" and len(Object) == 9:
            return True
        else:
            return False


