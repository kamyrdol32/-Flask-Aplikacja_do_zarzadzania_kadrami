import random
import string
import re

def passwordGenerator(stringlength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringlength))

Regex_Mail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

def checkMail(Mail):
    if (re.search(Regex_Mail, Mail)):
        return True
    else:
        return False