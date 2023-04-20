from tests.server_calls import auth_login_v2, auth_register_v2, clear_v2
from tests.helpers import clear_database
from time import sleep
"""
==============================================================
AUTH_LOGIN_V1 TESTS
==============================================================
"""

# Succesful login
def test_login_success():
    # Register and login functions should return different tokens
    reg_return_value = auth_register_v2("test", "test@test.com", "password")
    # 1 second sleep to allow for a time difference between generating tokens
    sleep(1)
    login_return_value = auth_login_v2("test@test.com", "password")
    print(login_return_value)
    assert reg_return_value["token"] != login_return_value["access_token"]

def test_login_multiple_success():
    reg_return_value_1 = auth_register_v2("test", "test@test.com", "password")["token"]
    # First user registered and logged in
    assert reg_return_value_1

    reg_return_value_2 = auth_register_v2("test", "test1@test.com", "password")["token"]
    # Second user registered and logged in
    assert reg_return_value_2

    # Unique id between both users
    assert reg_return_value_1 != reg_return_value_2

def test_login_incorrect_email():
    auth_register_v2("test", "test@test.com", "password")
    assert auth_login_v2("test2@test.com", "password")['detail'] == "Invalid input: Incorrect email or password."

def test_login_incorrect_email_and_password():
    auth_register_v2("test", "test@test.com", "password")
    assert auth_login_v2("test@test.com", "efef")['detail'] == "Invalid input: Incorrect email or password."

def test_login_incorrect_password():
    # Password is incorrect
    auth_register_v2("test", "test@test.com", "password")
    assert auth_login_v2("test@test.com", "eeffef")['detail'] == "Invalid input: Incorrect email or password."

    # Password is incorrect (and empty)
    auth_register_v2("test", "test1@test.com", "password")
    assert auth_login_v2("test1@test.com", "")['detail'][0]['msg'] == "field required"
