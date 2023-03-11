import unittest
# Authentication in Requests with HTTPBasicAuth
import requests
from requests.auth import HTTPBasicAuth

username = input('Please enter a username: ')
password = input('Please enter a password: ')

def check_lower(password):
    lower = any(user.islower() for user in password)
    return lower

def check_upper(password):
    upper = any(user.isupper() for user in password)
    return upper

def check_contains_digit(password):
    digit = any(user.isdigit() for user in  password)
    return digit

def final_password_checker(password):
    lower = password.check_lower()
    upper = password.check_upper()
    has_digit = password.check_contains_digit()

    try:
        if lower and upper and has_digit and len(password) >= 8:
            print('Successfully created a new password!')

    except:
        if not lower:
            print('Please check that you have a lowercase letter.')
        elif not upper:
            print('Please check that you have a uppercase letter.')
        elif not has_digit:
            print('Please check that you have a digit.')
        else:
            print('Please check if there is another error - double check all characters.')


auth = HTTPBasicAuth(username, password)

print(requests.get('https://httpbin.org/basic-auth/user/pass', auth=auth))

# assert 'Response [401]' in requests.get('https://httpbin.org/basic-auth/user/pass', auth=auth)
# requests.get('https://httpbin.org/basic-auth/user/pass', auth=auth).assertContains('Response [401]')

if 'Response [401]' in (requests.get('https://httpbin.org/basic-auth/user/pass', auth=auth)):
    print('SUCCESS')
else:
    print('NOT SUCCESS')