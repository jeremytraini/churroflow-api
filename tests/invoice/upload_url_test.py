from src.type_structure import *
from tests.server_calls import invoice_upload_url_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string, clear_database

"""
=====================================
/invoice/upload_url/v1 TESTS
=====================================
"""


def test_upload_url_valid_invoice():
    invoice = RemoteInvoice(name="My Invoice", url="https://raw.githubusercontent.com/A-NZ-PEPPOL/A-NZ-PEPPOL-BIS-3.0/master/Message%20examples/AU%20Invoice.xml")
    response = invoice_upload_url_v1(invoice.name, invoice.url)
    
    assert response['report_id'] >= 0

def test_upload_url_invalid_invoice_name():
    invalid_invoice_name = 'hellohellohellohellohellohellohellohellohellohellohellohello\
        hellohellohellohellohellohellohellohellohello'
    
    invoice = RemoteInvoice(name="My Invoice", url="https://raw.githubusercontent.com/A-NZ-PEPPOL/A-NZ-PEPPOL-BIS-3.0/master/Message%20examples/AU%20Invoice.xml")
    
    assert invoice_upload_url_v1(invalid_invoice_name, invoice.url)['detail'] == "Name cannot be longer than 100 characters"

def test_upload_url_invalid_url():
    invoice = RemoteInvoice(name="My Invoice", url="invalidurl")
    
    assert invoice_upload_url_v1(invoice.name, invoice.url)['detail'] == "Could not retrieve invoice from url"

def test_upload_url_invalid_format():
    invoice = RemoteInvoice(name="My Invoice", url="https://raw.githubusercontent.com/A-NZ-PEPPOL/A-NZ-PEPPOL-BIS-3.0/master/Message%20examples/AU%20Invoice.pdf")
    
    assert invoice_upload_url_v1(invoice.name, invoice.url)['detail'] == "URL does not point to plain text or XML data"
