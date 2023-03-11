from src.types import *
from tests.server_calls import report_json_report_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, invalidate_invoice

"""
=====================================
/report/json_report/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_json_valid_invoice():
    data = VALID_INVOICE_TEXT
    
    invoice = Invoice(name="My Invoice", source="text", data=data)

    report = report_json_report_v1(invoice)
    report = Report(**report)

    # Report id must be an integer
    assert isinstance(report.report_id, int)

    # Date generated must be a string
    assert isinstance(report.date_generated, str)

    # Checking for the name of the invoice
    assert report.invoice_name == "My Invoice"

    # Checking for raw invoice
    assert report.invoice_raw == invoice

    # Invoice hash must be a string
    assert isinstance(report.invoice_hash, str)

    # A valid invoice must be a valid report
    assert report.is_valid

    # A valid invoice should have 0 violations
    assert report.total_num_violations == 0
    
    # Check for wellformedness
    assert report.wellformedness.aspect == "wellformedness"
    assert report.wellformedness.is_valid == True
    assert report.wellformedness.num_rules_failed == 0
    assert report.wellformedness.num_violations == 0
    assert report.wellformedness.violations == []

    # Check for schema
    assert report.schemaEvaluation.aspect == "schema"
    assert report.schemaEvaluation.is_valid == True
    assert report.schemaEvaluation.num_rules_failed == 0
    assert report.schemaEvaluation.num_violations == 0
    assert report.schemaEvaluation.violations == []

    # Check for syntax
    assert report.syntax.aspect == "syntax"
    assert report.syntax.is_valid == True
    assert report.syntax.num_rules_failed == 0
    assert report.syntax.num_violations == 0
    assert report.syntax.violations == []

    # Check for PEPPOL
    assert report.peppol.aspect == "peppol"
    assert report.peppol.is_valid == True
    assert report.peppol.num_rules_failed == 0
    assert report.peppol.num_violations == 0
    assert report.peppol.violations == []

# Testing that a single rule fails when there is one error in the invoice
def test_syntax_single_violation():
    data = VALID_INVOICE_TEXT


# Testing that multiple violations are generated when there are multiple errors in the invoice
def test_syntax_multiple_violations_same_rule():
    data = VALID_INVOICE_TEXT


def test_syntax_multiple_violations_different_rules():
    data = VALID_INVOICE_TEXT
    

# Testing that a warning doesn't invalidate the report
def test_syntax_warning_doesnt_invalidate_report():
    data = VALID_INVOICE_TEXT
    
    
# Testing that a fatal error does invalidate the report
def test_syntax_fatal_error_invalidates_report():
    data = VALID_INVOICE_TEXT
    

