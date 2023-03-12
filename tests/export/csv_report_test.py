from src.type_structure import *
from tests.server_calls import export_csv_report_v1, invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, invalidate_invoice, clear_database

"""
=====================================
/report/csv_report/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_csv_valid_invoice():
    invoice = Invoice(name="My Invoice", source="text", data=VALID_INVOICE_TEXT)

    report_id = invoice_upload_text_v1(invoice.name, invoice.data)["report_id"]
    report_bytes = export_csv_report_v1(report_id)
    
    assert report_bytes
