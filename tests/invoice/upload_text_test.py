from src.type_structure import *
from tests.server_calls import invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/invoice/upload_text/v1 TESTS
=====================================
"""

def test_upload_text_valid_invoice():
    invoice = Invoice(name="My Invoice", data=VALID_INVOICE_TEXT)
    response = invoice_upload_text_v1(invoice.name, invoice.text)
    assert response['report_id'] >= 0
    
def test_upload_text_invalid_invoice():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the ABN, changing the content of the ABN
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
    invoice = Invoice(name="My Invoice", data=data)
    response = invoice_upload_text_v1(invoice.name, invoice.text)
    
    assert response['report_id'] >= 0
    
