from src.type_structure import *
from tests.server_calls import export_json_report_v1, invoice_upload_text_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, invalidate_invoice, clear_database

"""
=====================================
/report/json_report/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_json_valid_invoice():
    invoice = Invoice(name="My Invoice", source="text", data=VALID_INVOICE_TEXT)

    report_id = invoice_upload_text_v1(invoice.name, invoice.data)["report_id"]
    report = export_json_report_v1(report_id)
    report = Report(**report)

    # Report id must be an integer
    assert isinstance(report.report_id, int)

    # Date generated must be a string
    assert isinstance(report.date_generated, str)

    # Checking for the name of the invoice
    assert report.invoice_name == "My Invoice"

    # Checking for invoice text
    assert report.invoice_text == invoice.data

    # Invoice hash must be a string
    assert isinstance(report.invoice_hash, str)

    # A valid invoice must be a valid report
    assert report.is_valid

    # A valid invoice should have 0 violations
    assert report.total_errors == 0
    
    # Check for wellformedness
    assert report.wellformedness_evaluation.is_valid == True
    assert report.wellformedness_evaluation.num_rules_failed == 0
    assert report.wellformedness_evaluation.num_errors == 0
    assert report.wellformedness_evaluation.violations == []

    # Check for schema
    assert report.schema_evaluation.is_valid == True
    assert report.schema_evaluation.num_rules_failed == 0
    assert report.schema_evaluation.num_errors == 0
    assert report.schema_evaluation.violations == []

    # Check for syntax
    assert report.syntax_evaluation.is_valid == True
    assert report.syntax_evaluation.num_rules_failed == 0
    assert report.syntax_evaluation.num_errors == 0
    assert report.syntax_evaluation.violations == []

    # Check for PEPPOL
    assert report.peppol_evaluation.is_valid == True
    assert report.peppol_evaluation.num_rules_failed == 0
    assert report.peppol_evaluation.num_errors == 0
    assert report.peppol_evaluation.violations == []


