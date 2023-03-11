import unittest
# Authentication in Requests with HTTPBasicAuth
import requests
from requests.auth import HTTPBasicAuth
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from authentication.utils import generate_token

username = input('Please enter a username: ')
password = input('Please enter a password: ')

def check_lower(password):
    lower = any(pass.islower() for pass in password)
    return lower

def check_upper(password):
    upper = any(pass.isupper() for pass in password)
    return upper

def check_contains_digit(password):
    digit = any(pass.isdigit() for pass in  password)
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


# def check
#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)

#     # We expect exactly 0 rule to fail
#     assert wellformed_evaluation.num_rules_failed == 0

#     # We expect exactly 0 violations
#     assert wellformed_evaluation.num_violations == 0

#     # Thus there should be exactly 0 violations in the violation list
#     assert len(wellformed_evaluation.violations) == 0



def test_missing_username(username):
