from src.type_structure import *
from tests.server_calls import report_change_name_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/report/change_name/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_change_name():
    invoice = Invoice(name="My Invoice", source="text", data=VALID_INVOICE_TEXT)
    report_id = invoice_upload_text_v1(invoice.name, invoice.data)["report_id"]

    report = Report(**export_json_report_v1(report_id))
    
    # Checking for the old name of the invoice
    assert report.invoice_name == "My Invoice"

    report_change_name_v1(report_id, "New Name")
    report = Report(**export_json_report_v1(report_id))

    # Checking for the new name of the invoice
    assert report.invoice_name == "New Name"
