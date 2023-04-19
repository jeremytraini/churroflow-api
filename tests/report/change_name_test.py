from src.type_structure import *
from tests.server_calls import report_change_name_v2, export_json_report_v2, invoice_upload_text_v2, auth_register_v2
from tests.helpers import clear_database
from tests.constants import VALID_INVOICE_TEXT

"""
=====================================
/report/change_name/v1 TESTS
=====================================
"""
# Testing that the report was generated properly and matches input data
def test_change_name_valid():
    token = AuthReturnV2(**auth_register_v2("test", "test@test.com", "abc123")).token
    invoice = TextInvoice(name="My Invoice", text=VALID_INVOICE_TEXT)
    report_id = invoice_upload_text_v2(token, invoice.name, invoice.text)["report_id"]

    report = Report(**export_json_report_v2(token, report_id))
    
    # Checking for the old name of the invoice
    assert report.invoice_name == "My Invoice"

    report_change_name_v2(token, report_id, "New Name")
    report = Report(**export_json_report_v2(token, report_id))

    # Checking for the new name of the invoice
    assert report.invoice_name == "New Name"

def test_change_name_valid_upload_invalid_token():
    token = AuthReturnV2(**auth_register_v2("test", "test@test.com", "abc123")).token
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    assert report_change_name_v2("invalid", report_id, "New Name")['detail'] == "Invalid token, please login/register"

def test_change_name_not_owner():
    token = AuthReturnV2(**auth_register_v2("test", "test@test.com", "abc123")).token
    token2 = AuthReturnV2(**auth_register_v2("test", "test1@gmail.com", "abc123")).token
    report_id = invoice_upload_text_v2(token, "invoice", VALID_INVOICE_TEXT)["report_id"]
    
    assert report_change_name_v2(token2, report_id, "New Name")['detail'] == "You do not have permission to rename this report"

def test_change_name_long_invalid():
    token = AuthReturnV2(**auth_register_v2("test", "test@test.com", "abc123")).token
    invoice = TextInvoice(name="My Invoice", text=VALID_INVOICE_TEXT)
    report_id = invoice_upload_text_v2(token, invoice.name, invoice.text)["report_id"]

    report = Report(**export_json_report_v2(token, report_id))
    
    # Checking for the old name of the invoice
    assert report.invoice_name == "My Invoice"
    
    new_name = "hellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohellohello"
    assert report_change_name_v2(token, report_id, new_name)['detail'] == "New name is longer than 100 characters"

def test_change_name_invalid_report_id_negative():
    token = AuthReturnV2(**auth_register_v2("test", "test@test.com", "abc123")).token
    invoice = TextInvoice(name="My Invoice", text=VALID_INVOICE_TEXT)
    report_id = invoice_upload_text_v2(token, invoice.name, invoice.text)["report_id"]

    report = Report(**export_json_report_v2(token, report_id))
    
    # Checking for the old name of the invoice
    assert report.invoice_name == "My Invoice"

    assert report_change_name_v2(token, -1, "New Name")['detail'] == "Report id cannot be less than 0"

def test_change_name_invalid_report_id_not_found():
    token = AuthReturnV2(**auth_register_v2("test", "test@test.com", "abc123")).token
    invoice = TextInvoice(name="My Invoice", text=VALID_INVOICE_TEXT)
    report_id = invoice_upload_text_v2(token, invoice.name, invoice.text)["report_id"]

    report = Report(**export_json_report_v2(token, report_id))
    
    # Checking for the old name of the invoice
    assert report.invoice_name == "My Invoice"

    assert report_change_name_v2(token, 2937293, "New Name")['detail'] == "Report with id 2937293 not found"
