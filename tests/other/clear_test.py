from tests.server_calls import clear_v1

"""
=====================================
/clear/v1 TESTS
=====================================
"""


def test_clear_working():
    assert clear_v1("token")


def test_clear_after_generating_reportworking():
    assert clear_v1("token")

