from tests.server_calls import clear, auth_register_v1
from tests.constants import InputError, AuthError, AccessError

"""
==============================================================
AUTH_REGISTER_V1 TESTS
==============================================================
"""

# Test single registers with valid emails
def test_register_same_name():
    auth_user1 = auth_register_v1("test@test.com", "luciddreams14", "james", "bentley")
    auth_user2 = auth_register_v1("test@test.com", "luciddreams14", "james", "bentley")

    # Testing if user ID is unique
    assert auth_user1["token"] != auth_user2["token"]
    assert len(auth_user1) == 2

# Test multiple registers
def test_register_multiple_success():
    auth_register_v1("test@test.com", "www.www", "avani", "singh")
    auth_register_v1("test@test.com", "lisbon2424", "patrick", "jane")
    auth_register_v1("test@test.com", "janedoe", "lorelei", "martins")
    auth_register_v1("test@test.com", "knittingislife", "judy", "winters")

# Test Input errors for invalid email - failing regex match
def test_register_invalid_email():
    # Not matching regex after first character class
    assert auth_register_v1("chocoalate", "covered", "cupcake", "theory")['code'] == InputError

    # Doesn't have an @
    assert auth_register_v1("waterfordsgmail.com", "dasani2048", "water", "fords")['code'] == InputError

    # Fails last part of the regex - missing 2 alphabetic characters after '.'
    assert auth_register_v1("test@test.com", "paperboy", "caterina", "fall")['code'] == InputError

    # No email given
    assert auth_register_v1("", "paperboy", "caterina", "fall")['code'] == InputError

# Email is not unique - Raise Input Error
def test_register_duplicate_email():
    # Duplicate email example 1
    auth_register_v1("test@test.com", "iloveyou", "tammy", "turner")
    assert auth_register_v1("test@test.com", "iloveyou", "tammy", "Turner")['code'] == InputError

    # Duplicate email example 2 - only email is duplicated
    auth_register_v1("test@test.com", "dasani2048", "water", "fords")
    assert auth_register_v1("test@test.com", "dasani", "Uncle", "Iroh")['code'] == InputError

# Length of password is less than 6 characters
def test_register_short_passwords():
    assert auth_register_v1("test@test.com", "2048", "water", "fords")['code'] == InputError

    assert auth_register_v1("test@test.com", "LoVer", "tammy", "turner")['code'] == InputError

    assert auth_register_v1("test@test.com", "", "tammy", "turner")['code'] == InputError

# Name inputs not between 1-50 characters inclusive - invalid
def test_register_shortnames():
    # Both first and last names have no characters
    assert auth_register_v1("test@test.com", "iloveyou", "", "")['code'] == InputError

    # First name has no characters
    assert auth_register_v1("test@test.com", "iloveyou", "", "turner")['code'] == InputError

    # Last name has no characters
    assert auth_register_v1("test@test.com", "iloveyou", "tammy", "")['code'] == InputError

# Name inputs not between 1-50 characters inclusive - invalid
def test_register_longnames():
    # First and second names have too many characters
    assert auth_register_v1("test@test.com", "sammy234",
                        "samanthasamanthasamanthasamanthasamanthasamanthasamantha",
                        "sampson2345sampson2345sampson2345sampson2345sampson2345")['code'] == InputError

    # First name has too many characters
    assert auth_register_v1("test@test.com", "sammy234",
                        "samanthasamanthasamanthasamanthasamanthasamanthasamantha",
                        "sampson")['code'] == InputError

    # Last name has too many characters
    assert auth_register_v1("test@test.com", "sammy234",
                        "samantha",
                        "sampson2345sampson2345sampson2345sampson2345sampson2345")['code'] == InputError

def test_tokens_unique_after_clear():
    reg_return_value1 = auth_register_v1("test@test.com", "veryGOODpassword", "bob", "jenkins")

    clear_v1()
    reg_return_value2 = auth_register_v1("test@test.com", "veryGOODpassword", "bob", "jenkins")

    assert reg_return_value1["auth_user_id"] != reg_return_value2["auth_user_id"]
    assert reg_return_value1["token"] != reg_return_value2["token"]

def test_ensuring_token_invalidated_after_clear():
    auth_user1 = auth_register_v1("test@test.com", "veryGOODpassword", "bob", "jenkins")
    report_list_all_v1(auth_user1["token"])

    clear_v1()
    auth_user2 = auth_register_v1("test@test.com", "efigeyuifgiyueGVUY", "eufhgeu", "euiheui")

    print(auth_user1["token"])
    print(auth_user2["token"])

    assert report_list_all_v1(auth_user1["token"])["code"] == AccessError
