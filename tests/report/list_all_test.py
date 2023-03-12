from src.type_structure import *
from tests.server_calls import report_list_all_v1, invoice_upload_text_v1, export_json_report_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string, clear_database

"""
=====================================
/report/list_all/v1 TESTS
=====================================
"""

def test_list_all_one_report():
    invoice = Invoice(name="My Invoice", source="text", data=VALID_INVOICE_TEXT)
    invoice_upload_text_v1(invoice.name, invoice.data)

    report_ids = report_list_all_v1()
    report = export_json_report_v1(report_ids[0])
    report = Report(**report)

    # Checking for the name of the invoice
    assert report.invoice_name == "My Invoice"
    
    
    
def test_list_all_many_reports():
    invoice = Invoice(name="My Invoice", source="text", data=VALID_INVOICE_TEXT)
    invoice_upload_text_v1(invoice.name, invoice.data)
    invoice_upload_text_v1(invoice.name, invoice.data)
    invoice_upload_text_v1(invoice.name, invoice.data)

    report_ids = report_list_all_v1()
    
    assert len(report_ids) == 3
    
    report = export_json_report_v1(report_ids[0])
    report = Report(**report)
    
    # Checking for the name of the invoice
    assert report.invoice_name == "My Invoice"