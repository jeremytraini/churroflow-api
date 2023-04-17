from tests.server_calls import clear_v2, auth_register_v2, auth_login_v2

"""
=====================================
/clear/v1 TESTS
=====================================
"""


def test_clear_working():
    try:
        token = auth_register_v2("test", "churros@admin.com", "abc123")["token"]
        clear_v2(token)
    except KeyError:
        token = auth_login_v2("churros@admin.com", "abc123")["access_token"]
        clear_v2(token)

