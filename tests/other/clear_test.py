from tests.server_calls import clear_v1, auth_register_v2

"""
=====================================
/clear/v1 TESTS
=====================================
"""


def test_clear_working():
    clear_v1(auth_register_v2("clear_test_email1@test.com", "test123")["token"])

