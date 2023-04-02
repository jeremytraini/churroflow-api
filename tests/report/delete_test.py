from src.type_structure import *
from tests.server_calls import report_delete_invalid_token_v2, report_delete_v2, export_json_report_v1, invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/report/delete/v2 TESTS
=====================================
"""

def test_delete():
    report_id = invoice_upload_text_v1("invoice", VALID_INVOICE_TEXT)["report_id"]
    
    report_delete_v2(report_id)
    
    assert export_json_report_v1(report_id)["detail"] == f"Report with id {report_id} not found"

def test_delete_invalid_report_id_negative():
    assert report_delete_v2(-1)['detail'] == "Report id cannot be less than 0"

def test_delete_invalid_report_id_not_found():
    assert report_delete_v2(2937293)['detail'] == "Report with id 2937293 not found"

def test_delete_invalid_token():
    invoice = TextInvoice(name="My Invoice", source="text", text=VALID_INVOICE_TEXT)
    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]

    assert report_delete_invalid_token_v2(report_id)['detail'] == "Only admins can change the names of reports at the moment"
