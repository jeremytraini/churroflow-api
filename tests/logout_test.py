from tests.server_calls import auth_logout_v1, auth_login_v1
from tests.error import AccessError
from tests.server_calls import sample_post

"""
==============================================================
AUTH_LOGOUT_V1 TESTS
==============================================================
"""

def test_simple_logout(users):
    auth_logout_v1(users[0].token)
    assert channels_listall_v1(users[0].token)["code"] == AccessError

def test_register_logout_login(users):
    auth_logout_v1(users[0].token)
    same_auth_user = auth_login_v1(users[0].email, users[0].password)["token"]

    channels_listall_v1(same_auth_user)["channels"]

def test_logout_same_session_twice(users):
    auth_logout_v1(users[0].token)
    assert auth_logout_v1(users[0].token)["code"] == AccessError

def test_two_users_logout_one(users):
    auth_logout_v1(users[0].token)

    assert channels_listall_v1(users[0].token)["code"] == AccessError
    channels_listall_v1(users[1].token)["channels"]

def test_two_sessions_logout(users):
    same_auth_user = auth_login_v1(users[0].email, users[0].password)["token"]
    auth_logout_v1(users[0].token)

    assert channels_listall_v1(users[0])["code"] == AccessError
    channels_listall_v1(same_auth_user)["channels"]

    auth_logout_v1(same_auth_user)

    assert channels_listall_v1(users[0])["code"] == AccessError
    assert channels_listall_v1(same_auth_user)["code"] == AccessError

def test_two_sessions_logout_both(users):
    same_auth_user = auth_login_v1(users[0].email, users[0].password)["token"]
    auth_logout_v1(users[0].token)
    auth_logout_v1(same_auth_user)

    assert channels_listall_v1(users[0].token)["code"] == AccessError
    assert channels_listall_v1(same_auth_user)["code"] == AccessError
