import json
from src.type_structure import *
from tests.server_calls import export_html_report_v1, invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import replace_part_of_string, invalidate_invoice, clear_database

"""
=====================================
/report/html_report/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_html_valid_invoice():
    invoice = TextInvoice(name="My Invoice", text=VALID_INVOICE_TEXT)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report_bytes = export_html_report_v1(report_id)
    
    assert report_bytes


def test_html_text_invalid_peppol_invoice():
    data = invalidate_invoice(VALID_INVOICE_TEXT, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
    invoice = TextInvoice(name="My Invoice", text=data)
    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    
    report_bytes = export_html_report_v1(report_id)
    
    assert report_bytes

def test_html_text_invalid_wellformedness_invoice():
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

    invoice = TextInvoice(name="My Invoice", text=data)
    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report_bytes = export_html_report_v1(report_id)
    
    assert report_bytes

def test_html_invalid_id_negative():
    result = export_html_report_v1(-1)
    result = result.decode("utf-8")
    result = json.loads(result)
    assert result['detail'] == "Report id cannot be less than 0"

def test_html_invalid_id_not_found():
    result = export_html_report_v1(9332839283)
    result = result.decode("utf-8")
    result = json.loads(result)
    assert result['detail'] == "Report with id 9332839283 not found"
