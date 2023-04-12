from src.type_structure import *
from tests.server_calls import invoice_upload_text_v1, report_check_validity_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string, clear_database

"""
=====================================
/report/check_validity/v1 TESTS
=====================================
"""

def test_check_validity_one_report():
    report_id_valid = invoice_upload_text_v1("invoice", VALID_INVOICE_TEXT)["report_id"]
    
    invalid_invoice = VALID_INVOICE_TEXT[:1000]
    report_id_invalid = invoice_upload_text_v1("invoice", invalid_invoice)["report_id"]
    
    assert report_check_validity_v1(report_id_valid)["is_valid"] == True
    assert report_check_validity_v1(report_id_invalid)["is_valid"] == False

def test_check_validity_invalid_negative():
    assert report_check_validity_v1(-1)['detail'] == "Report id cannot be less than 0"

def test_check_validity_invalid_not_exist():
    
    assert report_check_validity_v1(320923904934)['detail'] == "Report with id 320923904934 not found"
