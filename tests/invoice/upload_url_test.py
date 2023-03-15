from src.type_structure import *
from tests.server_calls import invoice_upload_url_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/invoice/upload_url/v1 TESTS
=====================================
"""


def test_upload_url_valid_invoice():
    invoice = RemoteInvoice(name="My Invoice", url="https://raw.githubusercontent.com/A-NZ-PEPPOL/A-NZ-PEPPOL-BIS-3.0/master/Message%20examples/AU%20Invoice.xml")
    response = invoice_upload_url_v1(invoice.name, invoice.url)
    
    assert response['report_id'] >= 0

