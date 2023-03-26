from tests.server_calls import auth_login_v2, auth_register_v2, clear_v1
from time import sleep
"""
==============================================================
AUTH_LOGIN_V1 TESTS
==============================================================
"""

# Succesful login
def test_login_success():
    clear_v1()
    # Register and login functions should return different tokens
    reg_return_value = auth_register_v2("test@test.com", "password")
    # 1 second sleep to allow for a time difference between generating tokens
    sleep(1)
    login_return_value = auth_login_v2("test@test.com", "password")
    print(login_return_value)
    assert reg_return_value["token"] != login_return_value["token"]

def test_login_multiple_success():
    clear_v1()
    reg_return_value_1 = auth_register_v2("test@test.com", "password")["token"]
    # First user registered and logged in
    assert reg_return_value_1

    reg_return_value_2 = auth_register_v2("test1@test.com", "password")["token"]
    # Second user registered and logged in
    assert reg_return_value_2

    # Unique id between both users
    assert reg_return_value_1 != reg_return_value_2

def test_login_incorrect_email():
    clear_v1()
    auth_register_v2("test@test.com", "password")
    assert auth_login_v2("test2@test.com", "password")['detail'] == "Invalid input: No user with email test2@test.com."

def test_login_incorrect_email_and_password():
    clear_v1()
    auth_register_v2("test@test.com", "password")
    assert auth_login_v2("test@test.com", "efef")['detail'] == "Invalid input: Incorrect password."

def test_login_incorrect_password():
    clear_v1()
    # Password is incorrect
    auth_register_v2("test@test.com", "password")
    assert auth_login_v2("test@test.com", "eeffef")['detail'] == "Invalid input: Incorrect password."

    # Password is incorrect (and empty)
    auth_register_v2("test1@test.com", "password")
    assert auth_login_v2("test1@test.com", "")['detail'] == "Invalid input: Incorrect password."