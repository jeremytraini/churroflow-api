from src.types import *
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests


'''
Auth login and register functions.
'''

import re
import smtplib
from src.data_store import data_store
from src.helper import string_in_range
from src.error import InputError
from src.error import AccessError

def auth_login_v2(email, password):
    '''
    This function wraps auth_login_v1 to return an encoded token.

    Arguments:
        email (string)      - Email used to sign into the system. Must already exist.
        password (string)   - Password used to login into the specified user account,
                              must match existing password.

    Exceptions:
        InputError          - Occurs when user has put in incorrect password,
                              or email for non-existant account.

    Return Value:
        Returns token & auth_user_id when login is successful.
    '''

    auth_user_id = auth_login_v1(email, password)['auth_user_id']
    return {'token' : data_store.encode_user_jwt(auth_user_id), 'auth_user_id' : auth_user_id}

def auth_register_v2(email, password, name_first, name_last):
    '''
    This function wraps auth_register_v1 to return an encoded token.

    Arguments:
        email (string)      - Email used to register with the specified user. Must be unique.
        password (string)   - Password used to register with the specified user account.
        name_first (string) - First name of the user. Used to generate handle.
        name_last (string)  - Last name of the user. Used to generate handle.

    Exceptions:
        InputError          - Occurs when: email is not valid, email already exists
                              for another account, password is too short, first and/or
                              last name is not within a certain length.

    Return Value:
        Returns token & auth_user_id when registering is successful.
    '''

    auth_user_id = auth_register_v1(email, password, name_first, name_last)['auth_user_id']
    token = data_store.encode_user_jwt(auth_user_id)
    data_store.start_token_session(token) # check this
    return {'token' : token, 'auth_user_id' : auth_user_id}


def auth_logout_v1(token):
    '''
    This function logs a user out and expires their respective token.

    Arguments:
        token (string)      - Session token for user calling this function.

    Exceptions:

    Return Value:
        None.
    '''

    # Check if token is expired
    if not data_store.token_in_session(token):
        raise AccessError(description="Invalid access: Token is expired or otherwise invalid.")
    data_store.end_token_session(token)
    return {}

def auth_passwordreset_request_v1(email:str):
    '''
    This function sends an email to the specified email with a string to reset a user's password.

    Arguments:
        email (string)      - Email to send to.

    Exceptions:

    Return Value:
        None.
    '''

    # Get user id from email
    u_id = data_store.list_get_user_matching_email(email)
    if u_id == []:
        # If email doesn't exist we don't need to do anything
        return {}

    # Check user is already logged out of all current sessions, else we do nothing
    code:str = data_store.encode_user_jwt(u_id[0])
    if data_store.token_in_session(code):
        return {}

    code_truncate:str = code
    code_truncate = code_truncate[:10]

    # Send secret code (jwt but with new token secret) to email
    username:str = 'w09adingocomp1531@gmail.com'
    password:str = 'iteration3'
    body:str = f"Your code to reset your password is: {code_truncate}"
    message:str = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (username, email, 'Password Reset 1531', body)
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(username, email, message)
        server.close()
    except:
        pass

    return {}

def auth_passwordreset_reset_v1(reset_code:str, new_password:str):
    '''
    This function takes in a special code to reset a user's password, provided the code is correct.

    Arguments:
        reset_code (string)     - Special code to check if the user has the correct email.
        new_password (string)   - New password to reset to.

    Exceptions:
        InputError              - reset code is not valid, or password is too short.

    Return Value:
        None.
    '''
    # Decode token
    auth_user_id:int = data_store.find_user_from_truncated_jwt(reset_code)
    if auth_user_id == -1:
        raise InputError(description="Reset code is not a valid code.")

    if data_store.has_user_id(auth_user_id):
        if string_in_range(0, 5, new_password):
            raise InputError(description="Password entered is too short.")
        else:
            # Generate a new password and save it to data_store
            store = data_store.get()
            salt = data_store.gen_salt()
            password_hash = data_store.hash_password(new_password, salt)
            store['users'][auth_user_id]['password'] = password_hash
            data_store.set(store)
    else:
        raise InputError(description="Reset code is not a valid code.")

    return {}

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

    if not data_store.field_is_taken('email', email)['exists']:
        raise InputError(description="Invalid input: No user with email " + email + ".")

    user_id = data_store.field_is_taken('email', email)['id']

    if not data_store.field_is_taken('email', email)['exists']:
        raise InputError(description="Invalid input: No user with email " + email + ".")

    user_id = data_store.field_is_taken('email', email)['id']

    if not data_store.compare_hash(password, user_id):
        raise InputError(description="Invalid input: Incorrect password.")


    data_store.start_token_session(data_store.encode_user_jwt(user_id))

    return {'auth_user_id' : user_id}


def auth_register_v1(email, password, name_first, name_last):
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
        raise InputError(description="Email is invalid!")

    if data_store.field_is_taken('email', email)['exists']:
        store = data_store.get()
        for user in store['users']:
            if str(store['users'][user]['email']) == str(email) and store['users'][user]['is_deleted'] == False:
                raise InputError(description="Invalid input: Email " + email + " is already taken.")

    # Check if length of password is a valid length (> 5)
    if string_in_range(0, 5, password):
        raise InputError(description="Invalid input: Password is too short.")

    # Check if length of first name is a valid length
    if not string_in_range(1, 50, name_first):
        raise InputError(description="Invalid input: First name is an invalid length")

    # Check if length of last name is a valid length
    if not string_in_range(1, 50, name_last):
        raise InputError(description="Invalid input: Last name is an invalid length.")

    # Generate password hash
    salt = data_store.gen_salt()
    password_hash = data_store.hash_password(password, salt)

    # Generate user handle
    new_user_handle:str = generate_user_handle(name_first, name_last)

    make_global_owner = not bool(data_store.list_users())

    # Store the given data by finding an empty slot, then appending all information
    new_user_id:int = data_store.get_new_user_id()
    store = data_store.get()
    store['users'][new_user_id] = {
        'is_global_owner' : make_global_owner,
        'is_global_member' : False,
        'is_deleted' : False,
        'handle_str': new_user_handle,
        'first_name': name_first,
        'last_name': name_last,
        'email': email,
        'password': password_hash,
        'salt' : salt,
        'profile_img_url': 'http://www.bencloward.com/images/shaders_attenuation_normal.jpg',
        'notifications' : [],
        'user_stats': {
            'channels_joined': [],
            'dms_joined': [],
            'messages_sent': [],
            'involvement_rate': 0.0
        }}

    # Set the data in the database
    data_store.set(store)

    data_store.start_token_session(data_store.encode_user_jwt(new_user_id))

    # Return id once register is successful
    return {
        'auth_user_id': new_user_id,
    }

# Helper Functions

def generate_user_handle(name_first:str, name_last:str) -> str:
    '''
    This function generates a handle based on the first name and last name of the user.

    Arguments:
        name_first (str)   - User's inputted first name
        name_last (str)   - User's inputted last name

    Return Value:
        Returns a new_user_handle which is in the form of a string. Handles are expected
        to be alphanumerical characters in lower case, and will be under 20 characters
        unless there are duplicates. Otherwise, there will be a number at the end.
    '''

    # Grab data from our database
    stored_data = data_store.get()

    # Generate handle using list and appending first and last name, then truncating at 20 characters
    new_user_handle_list:str = []
    new_user_handle_list.append(name_first.lower())
    new_user_handle_list.append(name_last.lower())
    handle_merge:str = ''.join(new_user_handle_list)
    new_user_handle = ''.join(filter(str.isalnum, handle_merge))
    new_user_handle = new_user_handle[:20]

    # Check for duplicates
    handle_exists:bool = False
    for user_key in stored_data['users']:
        if stored_data['users'][user_key]['handle_str'] == new_user_handle and stored_data['users'][user_key]['is_deleted'] == False:
            handle_exists = True
            break

    # If duplicates exist, then concat an integer to the end until there exists no duplicates
    loop_count:int = 0
    original_handle_len = len(new_user_handle)
    while handle_exists:
        handle_exists = False
        new_user_handle = new_user_handle[:original_handle_len]
        new_user_handle += str(loop_count)

        # Check again if there exists no duplicates
        for user_key in stored_data['users']:
            if stored_data['users'][user_key]['handle_str'] == new_user_handle and stored_data['users'][user_key]['is_deleted'] == False:
                handle_exists = True
                break
        loop_count += 1

    # Return our generated handle
    return new_user_handle
