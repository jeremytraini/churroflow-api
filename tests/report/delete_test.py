from src.type_structure import *
from tests.server_calls import report_delete_v2, export_json_report_v1, invoice_upload_text_v2, auth_register_v2, clear_v1
from tests.constants import VALID_INVOICE_TEXT

"""
=====================================
/report/delete/v2 TESTS
=====================================
"""

def test_delete_valid():
    clear_v1()
    token = AuthReturnV2(**auth_register_v2("test@gmail.com", "abc123")).token
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    report_delete_v2(token, report_id)
    
    assert export_json_report_v1(report_id)["code"] == 500

def test_delete_invalid_upload():
    clear_v1()
    assert invoice_upload_text_v2("INVALID", "invoice", VALID_INVOICE_TEXT)['detail'] == "Invalid token, please login/register"

def test_delete_valid_upload_invalid_token():
    clear_v1()
    token = AuthReturnV2(**auth_register_v2("test@gmail.com", "abc123")).token
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    assert report_delete_v2("invalid", report_id)['detail'] == "Invalid token, please login/register"
