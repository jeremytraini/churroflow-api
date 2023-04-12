from src.type_structure import *
from tests.server_calls import report_list_by_v1, invoice_upload_text_v1, export_json_report_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string, clear_database

"""
=====================================
/report/list_by/v2 TESTS
=====================================
"""
    
def test_list_by_many_reports():
    invoice_upload_text_v1("invoice2", VALID_INVOICE_TEXT)
    invoice_upload_text_v1("invoice1", VALID_INVOICE_TEXT)
    invoice_upload_text_v1("invoice3", VALID_INVOICE_TEXT)

    report_ids1 = report_list_by_v1(OrderBy(table="invoice_name", is_ascending=True))["report_ids"]
    report_ids2 = report_list_by_v1(OrderBy(table="invoice_name", is_ascending=False))["report_ids"]
    
    assert len(report_ids1) == len(report_ids2) == 3
    assert report_ids1[0] == report_ids2[-1]
    
    report = export_json_report_v1(report_ids1[0])
    report = Report(**report)
    
    # Checking for the name of the first invoice
    assert report.invoice_name == "invoice1"
