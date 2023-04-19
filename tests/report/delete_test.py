from src.type_structure import *
from tests.server_calls import report_delete_v2, export_json_report_v1, invoice_upload_text_v2, auth_register_v2
from tests.helpers import clear_database
from tests.constants import VALID_INVOICE_TEXT

"""
=====================================
/report/delete/v2 TESTS
=====================================
"""

def test_delete_valid():
    token = auth_register_v2("test", "test@test.com", "abc123")["token"]
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    report_delete_v2(token, report_id)
    
    assert export_json_report_v1(report_id)["detail"] == f"Report with id {report_id} not found"

def test_delete_invalid_report_id_negative():
    token = auth_register_v2("test", "test@test.com", "abc123")["token"]
    assert report_delete_v2(token, -1)['detail'] == "Report id cannot be less than 0"

def test_delete_invalid_report_id_not_found():
    token = auth_register_v2("test", "test@test.com", "abc123")["token"]
    assert report_delete_v2(token, 2937293)['detail'] == "Report with id 2937293 not found"

def test_delete_invalid_upload():
    assert invoice_upload_text_v2("INVALID", "invoice", VALID_INVOICE_TEXT)['detail'] == "Invalid token, please login/register"

def test_delete_valid_upload_invalid_token():
    token = auth_register_v2("test", "test@test.com", "abc123")["token"]
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    assert report_delete_v2("invalid", report_id)['detail'] == "Invalid token, please login/register"

def test_delete_invalid_not_owner():
    token = auth_register_v2("test", "test@test.com", "abc123")["token"]
    token2 = auth_register_v2("test", "test_delete_invalid_not_owner1@gmail.com", "abc123")["token"]
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    assert report_delete_v2(token2, report_id)['detail'] == "You do not have permission to delete this report"
