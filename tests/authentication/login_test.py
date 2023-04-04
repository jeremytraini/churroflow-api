from tests.server_calls import auth_login_v2, auth_register_v2, clear_v1
from time import sleep
"""
==============================================================
AUTH_LOGIN_V1 TESTS
==============================================================
"""

# Succesful login
def test_login_success():
    # Register and login functions should return different tokens
    reg_return_value = auth_register_v2("test@test.com", "password")
    # 1 second sleep to allow for a time difference between generating tokens
    sleep(1)
    login_return_value = auth_login_v2("test@test.com", "password")
    print(login_return_value)
    assert reg_return_value["token"] != login_return_value["access_token"]
    clear_v1(reg_return_value["token"])

def test_login_multiple_success():
    reg_return_value_1 = auth_register_v2("test@test.com", "password")["token"]
    # First user registered and logged in
    assert reg_return_value_1

    reg_return_value_2 = auth_register_v2("test1@test.com", "password")["token"]
    # Second user registered and logged in
    assert reg_return_value_2

    # Unique id between both users
    assert reg_return_value_1 != reg_return_value_2
    clear_v1(reg_return_value_1)

def test_login_incorrect_email():
    token = auth_register_v2("test@test.com", "password")["token"]
    assert auth_login_v2("test2@test.com", "password")['detail'] == "Invalid input: Incorrect email or password."
    clear_v1(token)

def test_login_incorrect_email_and_password():
    token = auth_register_v2("test@test.com", "password")["token"]
    assert auth_login_v2("test@test.com", "efef")['detail'] == "Invalid input: Incorrect email or password."
    clear_v1(token)

def test_login_incorrect_password():
    # Password is incorrect
    token = auth_register_v2("test@test.com", "password")["token"]
    assert auth_login_v2("test@test.com", "eeffef")['detail'] == "Invalid input: Incorrect email or password."

    # Password is incorrect (and empty)
    auth_register_v2("test1@test.com", "password")
    assert auth_login_v2("test1@test.com", "")['detail'][0]['msg'] == "field required"
    clear_v1(token)