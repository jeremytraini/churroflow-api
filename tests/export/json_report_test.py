from src.type_structure import *
from tests.server_calls import export_json_report_v1, invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, invalidate_invoice, clear_database

"""
=====================================
/export/json_report/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_json_valid_invoice():
    data = VALID_INVOICE_TEXT
    
    invoice = TextInvoice(name="My Invoice", text=data)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report = export_json_report_v1(report_id)
    report = Report(**report)

    # Report id must be an integer
    assert isinstance(report.report_id, int)

    # Date generated must be a string
    assert isinstance(report.date_generated, str)

    # Checking for the name of the invoice
    assert report.invoice_name == "My Invoice"

    # Invoice hash must be a string
    assert isinstance(report.invoice_hash, str)

    # A valid invoice must be a valid report
    assert report.is_valid

    # A valid invoice should have 0 violations
    assert report.total_warnings == 0
    assert report.total_errors == 0
    
    # Check for wellformedness
    assert report.wellformedness_evaluation.is_valid == True
    assert report.wellformedness_evaluation.num_rules_failed == 0
    assert report.wellformedness_evaluation.num_errors == 0
    assert report.wellformedness_evaluation.num_warnings == 0
    assert len(report.wellformedness_evaluation.violations) == 0

    # Check for schema
    assert report.schema_evaluation.is_valid == True
    assert report.schema_evaluation.num_rules_failed == 0
    assert report.schema_evaluation.num_errors == 0
    assert report.schema_evaluation.num_warnings == 0
    assert len(report.schema_evaluation.violations) == 0

    # Check for syntax
    assert report.syntax_evaluation.is_valid == True
    assert report.syntax_evaluation.num_rules_failed == 0
    assert report.syntax_evaluation.num_errors == 0
    assert report.syntax_evaluation.num_warnings == 0
    assert len(report.syntax_evaluation.violations) == 0

    # Check for PEPPOL
    assert report.peppol_evaluation.is_valid == True
    assert report.peppol_evaluation.num_rules_failed == 0
    assert report.peppol_evaluation.num_errors == 0
    assert report.syntax_evaluation.num_warnings == 0
    assert len(report.peppol_evaluation.violations) == 0
    
def test_json_unique_id():
    data = VALID_INVOICE_TEXT

    # Creating 2 invoices
    invoice1 = TextInvoice(name="Invoice01", text=data)
    invoice2 = TextInvoice(name="Invoice02", text=data)

    # Creating 2 reports
    report_id1 = invoice_upload_text_v1(invoice1.name, invoice1.text)["report_id"]
    report1 = export_json_report_v1(report_id1)
    report1 = Report(**report1)
    report_id2 = invoice_upload_text_v1(invoice2.name, invoice2.text)["report_id"]
    report2 = export_json_report_v1(report_id2)
    report2 = Report(**report2)

    # Check that the report_id is not the same
    assert report1.report_id != report2.report_id

    # Check names of the invoice
    assert report1.invoice_name == "Invoice01"
    assert report2.invoice_name == "Invoice02"

    
# Testing that a single rule fails when there is one error in the invoice
def test_json_single_violation():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the currency code
    data = invalidate_invoice(data, "attrib", "cbc:Amount", "currencyID", "TEST", 1)
    
    invoice = TextInvoice(name="Invoice Test", text=data)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report = export_json_report_v1(report_id)
    report = Report(**report)

    # Check the name of the invoice
    assert report.invoice_name == "Invoice Test"

    # Invalidating a currency code is fatal so report must not be valid
    assert report.is_valid == False

    # 1 error from syntax and 2 errors from peppol
    assert report.total_warnings == 0
    assert report.total_errors == 3

    # Check for wellformedness
    assert report.wellformedness_evaluation.is_valid == True
    assert report.wellformedness_evaluation.num_rules_failed == 0
    assert report.wellformedness_evaluation.num_errors == 0
    assert report.wellformedness_evaluation.num_warnings == 0
    assert len(report.wellformedness_evaluation.violations) == 0

    # Check for schema
    assert report.schema_evaluation.is_valid == True
    assert report.schema_evaluation.num_rules_failed == 0
    assert report.schema_evaluation.num_errors == 0
    assert report.schema_evaluation.num_warnings == 0
    assert len(report.schema_evaluation.violations) == 0

    # Check for syntax
    assert report.syntax_evaluation.is_valid == False
    assert report.syntax_evaluation.num_rules_failed == 1
    assert report.syntax_evaluation.num_errors == 1
    assert report.syntax_evaluation.num_warnings == 0
    assert len(report.syntax_evaluation.violations) == 1

    # Check for PEPPOL
    assert report.peppol_evaluation.is_valid == False
    assert report.peppol_evaluation.num_rules_failed == 2
    assert report.peppol_evaluation.num_errors == 2
    assert report.syntax_evaluation.num_warnings == 0
    assert len(report.peppol_evaluation.violations) == 2
    
# Testing that multiple violations are generated when there are multiple errors in the invoice
def test_json_multiple_violations_same_rule():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the 2 ABNs
    data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 1", 1)
    data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 2", 2)
    
    invoice = TextInvoice(name="Invoice Test", text=data)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report = export_json_report_v1(report_id)
    report = Report(**report)

    # Invalidating an ABN is only a warning so report must still be valid
    assert report.is_valid

    # Invalidating 2 ABNs - 2 violation
    assert report.total_warnings == 2
    assert report.total_errors == 0

    # Check for wellformedness
    assert report.wellformedness_evaluation.is_valid == True
    assert report.wellformedness_evaluation.num_rules_failed == 0
    assert report.wellformedness_evaluation.num_errors == 0
    assert report.wellformedness_evaluation.num_warnings == 0
    assert len(report.wellformedness_evaluation.violations) == 0

    # Check for schema
    assert report.schema_evaluation.is_valid == True
    assert report.schema_evaluation.num_rules_failed == 0
    assert report.schema_evaluation.num_errors == 0
    assert report.schema_evaluation.num_warnings == 0
    assert len(report.schema_evaluation.violations) == 0

    # Check for syntax
    assert report.syntax_evaluation.is_valid == True
    assert report.syntax_evaluation.num_rules_failed == 0
    assert report.syntax_evaluation.num_errors == 0
    assert report.syntax_evaluation.num_warnings == 0
    assert len(report.syntax_evaluation.violations) == 0

    # Check for PEPPOL
    assert report.peppol_evaluation.is_valid == True
    assert report.peppol_evaluation.num_rules_failed == 1
    assert report.peppol_evaluation.num_errors == 0
    assert report.peppol_evaluation.num_warnings == 2
    assert len(report.peppol_evaluation.violations) == 2
    
def test_json_multiple_violations_different_rules():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the 2 ABNs (PEPPOL)
    data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 1", 1)
    data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 2", 2)

    # Invalidating the 2 Country/IdentificationCode (Syntax)
    data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'TEST', 1)
    data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'TEST', 2)
    
    invoice = TextInvoice(name="Invoice Test", text=data)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report = export_json_report_v1(report_id)
    report = Report(**report)

    # Invalidating an Country/IdentificationCode is fatal so report must be invalid
    assert report.is_valid == False

    # 2 Warnings and 2 Errors
    assert report.total_warnings == 2
    assert report.total_errors == 2

    # Check for wellformedness
    assert report.wellformedness_evaluation.is_valid == True
    assert report.wellformedness_evaluation.num_rules_failed == 0
    assert report.wellformedness_evaluation.num_errors == 0
    assert report.wellformedness_evaluation.num_warnings == 0
    assert len(report.wellformedness_evaluation.violations) == 0

    # Check for schema
    assert report.schema_evaluation.is_valid == True
    assert report.schema_evaluation.num_rules_failed == 0
    assert report.schema_evaluation.num_errors == 0
    assert report.schema_evaluation.num_warnings == 0
    assert len(report.schema_evaluation.violations) == 0

    # Check for syntax
    assert report.syntax_evaluation.is_valid == False
    assert report.syntax_evaluation.num_rules_failed == 1
    assert report.syntax_evaluation.num_errors == 2
    assert report.syntax_evaluation.num_warnings == 0
    assert len(report.syntax_evaluation.violations) == 2

    # Check for PEPPOL
    assert report.peppol_evaluation.is_valid == True
    assert report.peppol_evaluation.num_rules_failed == 1
    assert report.peppol_evaluation.num_errors == 0
    assert report.peppol_evaluation.num_warnings == 2
    assert len(report.peppol_evaluation.violations) == 2
    
# Testing invalid wellformedness
def test_json_invalid_wellformedness():
    data = VALID_INVOICE_TEXT
    
    # Removing a closing tag
    data = remove_part_of_string(data, 11530, 11540)
    
    invoice = TextInvoice(name="Invoice Test", text=data)

    report_id = invoice_upload_text_v1(invoice.name, invoice.text)["report_id"]
    report = export_json_report_v1(report_id)
    report = Report(**report)

    # Removing a closing tag is a fatal error
    assert report.is_valid == False

    # Violating 1 rule
    assert report.total_warnings == 0
    assert report.total_errors == 1

    # Check for wellformedness
    assert report.wellformedness_evaluation.is_valid == False
    assert report.wellformedness_evaluation.num_rules_failed == 1
    assert report.wellformedness_evaluation.num_errors == 1
    assert report.wellformedness_evaluation.num_warnings == 0
    assert len(report.wellformedness_evaluation.violations) == 1

    # Invalid wellformedness means no schema, syntax and peppol evaluation
    assert report.schema_evaluation == None
    assert report.syntax_evaluation == None
    assert report.peppol_evaluation == None

def test_json_invalid_id_negative():
    
    assert export_json_report_v1(-1)['detail'] == "Report id cannot be less than 0"

def test_json_invalid_id_not_found():
    
    assert export_json_report_v1(9332839283)['detail'] == "Report with id 9332839283 not found"
    