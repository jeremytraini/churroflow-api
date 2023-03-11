from src.type_structure import *
from tests.server_calls import invoice_upload_file_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/invoice/upload_file/v1 TESTS
=====================================
"""

def test_upload_file_valid_invoice():
    invoice = Invoice(name="My Invoice", filename="src/AUInvoice.xml")
    response = invoice_upload_file_v1(invoice.name, invoice.filename)
    
    assert response['report_id'] >= 0
