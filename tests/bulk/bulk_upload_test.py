from tests.server_calls import health_check_v1

"""
=====================================
/invoice/file_upload_bulk/v1 TESTS
=====================================
"""

def test_health_check_working():
    assert health_check_v1()['is_alive'] == True
    

