from src.type_structure import *
from tests.server_calls import report_list_by_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/report/list_by/v1 TESTS
=====================================
"""
    
def test_list_by_many_reports():
    invoice_upload_text_v1("invoice1", VALID_INVOICE_TEXT)
    invoice_upload_text_v1("invoice2", VALID_INVOICE_TEXT)
    invoice_upload_text_v1("invoice3", VALID_INVOICE_TEXT)

    report_ids = report_list_by_v1(OrderBy("invoice_name", "asc"))
    
    assert len(report_ids) == 3
    
    report = export_json_report_v1(report_ids[0])
    report = Report(**report)
    
    # Checking for the name of the invoice
    assert report.invoice_name == "My Invoice"
