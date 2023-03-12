from src.type_structure import *
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, replace_part_of_string
from tests.server_calls import invoice_file_upload_bulk_v1

"""
=====================================
/invoice/file_upload_bulk/v1 TESTS
=====================================
"""

def test_bulk_upload_valid():
    data = VALID_INVOICE_TEXT
    invoice_valid = Invoice(name="My Invoice", source="text", data=data)

    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
    data = invalidate_invoice(data, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
    invoice_schema = Invoice(name="My Invoice", source="text", data=data)

    data = invalidate_invoice(VALID_INVOICE_TEXT, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
    invoice_peppol = Invoice(name="My Invoice", source="text", data=data)
    
    data = invalidate_invoice(VALID_INVOICE_TEXT, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    invoice_syntax = Invoice(name="My Invoice", source="text", data=data)
    
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

    invoice_wellformedness = Invoice(name="My Invoice", source="text", data=data)
    
    invoices = [invoice_valid, invoice_schema, invoice_peppol, invoice_syntax, invoice_wellformedness]
    
    report_ids = invoice_file_upload_bulk_v1(invoices)
    
    # checking that the number of report_ids returned is the same as the number of invoices inputted
    assert len(report_ids) == len(invoices)
    
