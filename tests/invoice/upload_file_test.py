from src.type_structure import *
from tests.server_calls import invoice_upload_file_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string, clear_database

"""
=====================================
/invoice/upload_file/v1 TESTS
=====================================
"""

def test_upload_file_valid_invoice():
    response = invoice_upload_file_v1("tests/example_files/AUInvoice.xml")
    
    assert response['report_id'] >= 0

def test_upload_file_invalid_invoice_format():
    
    assert invoice_upload_file_v1("tests/example_files/AUInvoice.txt")['detail'] == "Invoice file type is not XML"
