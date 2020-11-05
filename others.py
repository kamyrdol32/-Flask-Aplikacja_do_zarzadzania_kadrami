import random
import string
import re

def passwordGenerator(stringlength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringlength))

Regex_Mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
Regex_Number = '^(\+48 |0)[1-9]( \d){9}$'

def check(Type, String):
    if Type == "Mail":
        if (re.search(Regex_Mail, String)):
            return True
        else:
            return False
    elif Type == "Number":
        if (re.search(Regex_Number, String)):
            return True
        else:
            return False