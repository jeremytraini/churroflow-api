from tests.server_calls import clear_v1, auth_register_v1

"""
==============================================================
AUTH_REGISTER_V1 TESTS
==============================================================
"""

# Test single registers with valid emails
def test_register_unique_id_valid():
    clear_v1()
    auth_user1 = auth_register_v1("test@test.com", "luciddreams14")
    auth_user2 = auth_register_v1("test1@test.com", "luciddreams14")
    print(auth_user1)
    # Testing if user ID is unique
    assert auth_user1["auth_user_id"] != auth_user2["auth_user_id"]
    assert len(auth_user1) == 1

# Test multiple registers
def test_register_multiple_success():
    clear_v1()
    auth_user1 =auth_register_v1("test@test.com", "www.www")["auth_user_id"]
    auth_user2 =auth_register_v1("test1@test.com", "lisbon2424")["auth_user_id"]
    auth_user3 =auth_register_v1("test2@test.com", "janedoe")["auth_user_id"]
    auth_user4 =auth_register_v1("test3@test.com", "knittingislife")["auth_user_id"]
    assert auth_user1 != auth_user2 != auth_user3 != auth_user4

# Test Input errors for invalid email - failing regex match
def test_register_invalid_email():
    clear_v1()
    # Not matching regex after first character class
    assert auth_register_v1("chocoalate", "covered")['detail'] == "Email is invalid!"

    # Doesn't have an @
    assert auth_register_v1("waterfordsgmail.com", "dasani2048")['detail'] == "Email is invalid!"

    # Fails last part of the regex - missing 2 alphabetic characters after '.'
    assert auth_register_v1("test@test.c", "paperboy")['detail'] == "Email is invalid!"

    # No email given
    assert auth_register_v1("", "paperboy")['detail'] == "Email is invalid!"

# Email is not unique - Raise Input Error
def test_register_duplicate_email():
    clear_v1()
    # Duplicate email example 1
    auth_register_v1("test@test.com", "iloveyou")
    assert auth_register_v1("test@test.com", "iloveyou")['detail'] == "Invalid input: Email test@test.com is already taken."

    # Duplicate email example 2 - only email is duplicated
    auth_register_v1("test1@test.com", "dasani2048")
    assert auth_register_v1("test1@test.com", "dasani")['detail'] == "Invalid input: Email test1@test.com is already taken."

# Length of password is less than 6 characters
def test_register_short_passwords():
    clear_v1()
    assert auth_register_v1("test@test.com", "2048")['detail'] == "Invalid input: Password is too short."

    assert auth_register_v1("test1@test.com", "LoVer")['detail'] == "Invalid input: Password is too short."

    assert auth_register_v1("test2@test.com", "")['detail'] == "Invalid input: Password is too short."

