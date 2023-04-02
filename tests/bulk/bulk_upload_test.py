from src.type_structure import *
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, replace_part_of_string
from tests.server_calls import invoice_bulk_upload_file_v1

"""
=====================================
/invoice/file_upload_bulk/v1 TESTS
=====================================
"""

# def test_bulk_upload_valid():
#     data = VALID_INVOICE_TEXT
#     invoice_valid = TextInvoice(name="My Invoice", text=data)

#     data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
#     data = invalidate_invoice(data, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
#     invoice_schema = TextInvoice(name="My Invoice", text=data)

#     data = invalidate_invoice(VALID_INVOICE_TEXT, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
#     invoice_peppol = TextInvoice(name="My Invoice", text=data)
    
#     data = invalidate_invoice(VALID_INVOICE_TEXT, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
#     invoice_syntax = TextInvoice(name="My Invoice", text=data)
    
#     data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

#     invoice_wellformedness = TextInvoice(name="My Invoice", text=data)
    
#     invoices = [invoice_valid, invoice_schema, invoice_peppol, invoice_syntax, invoice_wellformedness]
    
#     # report_ids = invoice_bulk_upload_file_v1(invoices)
#     report_ids = invoice_bulk_upload_file_v1("tests/example_files/AUInvoice.xml", "tests/example_files/AUInvoice.xml")
    
#     # checking that the number of report_ids returned is the same as the number of invoices inputted
#     assert len(report_ids) == 2
    
