from src.database import Users, IntegrityError, DoesNotExist
from src.helper import string_in_range
from src.error import InputError
from src.type_structure import *
import hashlib
import re

'''
Auth login and register functions.
'''

def auth_login_v1(email, password):
    '''
    This function uses user-inputted login data to log a user into the system.

    Arguments:
        email (string)      - Email used to sign into the system. Must already exist.
        password (string)   - Password used to login into the specified user account,
                              must match existing password.

    Exceptions:
        InputError          - Occurs when user has put in incorrect password, or email
                              for non-existant account.

    Return Value:
        Returns auth_user_id when login is successful, i.e. there are no InputErrors.
        Return value gives index of user account within the system.
    '''
    try:
        user = Users.get(email=email)
    except DoesNotExist:
        raise InputError(status_code=400, detail="Invalid input: No user with email " + email + ".")
    
    if user.password_hash != hashlib.sha256(password.encode("utf-8")).hexdigest():
        raise InputError(status_code=400, detail="Invalid input: Incorrect password.")


    # data_store.start_token_session(data_store.encode_user_jwt(user_id))

    return {'auth_user_id' : user.id}


def auth_register_v1(email, password):
    '''
    This function registers a user into the system by getting their details.

    Arguments:
        email (string)      - Email used to register with the specified user. Must be unique.
        password (string)   - Password used to register with the specified user account.
        name_first (string) - First name of the user. Used to generate handle.
        name_last (string)  - Last name of the user. Used to generate handle.

    Exceptions:
        InputError          - Occurs when: email is not valid, email already exists for another
                              account, password is too short, first and/or last name is not
                              within a certain length.

    Return Value:
        Returns auth_user_id when registering is successful, i.e. there are no InputErrors.
        Return value gives index of user account within the system.
    '''

    # Checks for valid input (check back to the spec to see which errors are there)
    # Check for valid email, i.e. has @ in the string
    regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    if re.fullmatch(regex, email) is None:
        raise InputError(status_code=400, detail="Email is invalid!")

    # Check if length of password is a valid length (> 5)
    if string_in_range(0, 5, password):
        raise InputError(status_code=400, detail="Invalid input: Password is too short.")

    # Generate password hash
    # salt = data_store.gen_salt()
    password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    try:
        user = Users.create(email=email, password_hash=password_hash)
    except IntegrityError:
        # duplicate email
        raise InputError(status_code=400, detail="Invalid input: Email " + email + " is already taken.")
    
    # Return id once register is successful
    return {
        'auth_user_id': user.id,
    }