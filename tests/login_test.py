import pytest
import unittest
from tests.server_calls import auth_login_v1, auth_register_v1
from tests.error import InputError
import pytest
# from src.data_store import data_store



"""
==============================================================
AUTH_LOGIN_V1 TESTS
==============================================================
"""

# Succesful login
def test_login_success():
    # clear()
    loginDict = {}
    # Register and login functions should return same id for same user
    reg_return_value = auth_register_v1("test@test.com", "password", "bob", "brown")
    login_return_value = auth_login_v1("test@test.com", "password")
    assert reg_return_value["token"] != login_return_value["token"]

def test_login_multiple_success():
    reg_return_value_1 = auth_register_v1("test@test.com", "password", "bob", "jenkins")["token"]
    # First user registered and logged in
    assert reg_return_value_1

    reg_return_value_2 = auth_register_v1("test@test.com", "password", "bob", "brown")["token"]
    # Second user registered and logged in
    assert reg_return_value_2

    # Unique id between both users
    assert reg_return_value_1 != reg_return_value_2

def test_login_incorrect_email():
    auth_register_v1("test@test.com", "password", "bob", "brown")
    print(auth_login_v1("test2@test.com", "password")['code'])
    assert auth_login_v1("test2@test.com", "password")['code'] == InputError

def test_login_incorrect_email_and_password():
    auth_register_v1("test@test.com", "password", "bob", "brown")
    assert auth_login_v1("test@test.com", "efef")['code'] == InputError

def test_login_incorrect_password():
    # Password is incorrect
    auth_register_v1("test@test.com", "password", "bob", "brown")
    assert auth_login_v1("test@test.com", "eeffef")['code'] == InputError

    # Password is incorrect (and empty)
    auth_register_v1("test@test.com", "password", "bob", "brown")
    assert auth_login_v1("test@test.com", "")['code'] == InputError