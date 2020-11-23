from app import *

import random
import string
import re

def sendWelcomeMail(recipient, password, companyName):
    msg = Message('Aplikacja do zarzadzania kadrami', sender='kamyrdol32test@gmail.com', recipients=[recipient])
    msg.html = "<h3>Witaj " + recipient + "</h3><br>Zostałeś zarejestrowany w firmie " + companyName + ", witamy na pokładzie!<br>Mamy nadzieję, że Ci sie tu spodoba.<br><br>Poniżej przekazujemy Ci Twoje prywatne hasło do przeprowadzenia procesu pierwszego logowania.<br><br><b>Login:</b> " + recipient + "<br><b>Hasło:</b> " + password + "<br><br>Rekomendujemy natychmiastową zmianę hasła po logowaniu.<br><b>Bezpieczeństwo przede wszystkim!</b><br><br>Zapraszamy<br>http://evgaming.duckdns.org:70/"
    mail.send(msg)

def passwordGenerator(stringlength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringlength))


Regex_Mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
Regex_Number = '^(\+48 |0)[1-9]( \d){9}$'

def check(Type, String):
    if Type == "Mail":
        if re.search(Regex_Mail, String):
            return True
        else:
            return False
    elif Type == "Number":
        if re.search(Regex_Number, String):
            return True
        else:
            return False
