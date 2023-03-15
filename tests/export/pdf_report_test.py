from src.type_structure import *
from tests.server_calls import export_pdf_report_v1, invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT

"""
=====================================
/report/pdf_report/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_pdf_valid_invoice():
    invoice = TextInvoice(name="My Invoice", source="text", text=VALID_INVOICE_TEXT)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report_bytes = export_pdf_report_v1(report_id)
    
    assert report_bytes
