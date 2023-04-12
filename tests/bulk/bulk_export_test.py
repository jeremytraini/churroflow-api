from src.type_structure import *
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, replace_part_of_string, clear_database
from tests.server_calls import export_bulk_json_reports_v1, invoice_upload_text_v1

"""
=====================================
/report/bulk_export/v1 TESTS
=====================================
"""

def test_bulk_export_valid():
    data = VALID_INVOICE_TEXT
    invoice_valid = TextInvoice(name="My Invoice", text=data)

    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
    data = invalidate_invoice(data, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
    invoice_schema = TextInvoice(name="My Invoice", text=data)

    data = invalidate_invoice(VALID_INVOICE_TEXT, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
    invoice_peppol = TextInvoice(name="My Invoice", text=data)
    
    data = invalidate_invoice(VALID_INVOICE_TEXT, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    invoice_syntax = TextInvoice(name="My Invoice", text=data)
    
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

    invoice_wellformedness = TextInvoice(name="My Invoice", text=data)
    
    report_ids = []
    for invoice in [invoice_valid, invoice_schema, invoice_peppol, invoice_syntax, invoice_wellformedness]:
        report_ids.append(invoice_upload_text_v1(invoice.name, invoice.text)["report_id"])
    
    invoices = export_bulk_json_reports_v1(report_ids)["reports"] # type: ignore
    
    # Checking that the number of exports returned is the same as the number of invoices inputted
    assert len(report_ids) == len(invoices)
    # assert len(exports) == len(report_ids) == len(invoices)
