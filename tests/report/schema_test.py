from src.type_structure import Invoice, Evaluation
from tests.server_calls import report_schema_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import *

"""
=====================================
/report/schemavalid/v1 TESTS
=====================================
"""
def test_schema_valid():
    # Replacing the tags but making sure they are valid
    data = VALID_INVOICE_TEXT

    invoice = Invoice(name="My Invoice", source="text", data=data)

    schema_evaluation = report_schema_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    # We expect exactly 0 rule to fail due to the corrections
    assert schema_evaluation.num_rules_failed == 0

    # We expect exactly 0 violation due to the corrections
    assert schema_evaluation.num_errors == 0

    # Thus there should be exactly 0 violation in the violation list
    assert len(schema_evaluation.violations) == 0

def test_schema_tag_name_invalid():
    # Invalidating the tags so that it doesn't match the schema
    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)
    data = invalidate_invoice(data, "tag", "cac:BillingReference", "", "cac:BillingReferencee", 1)

    invoice = Invoice(name="My Invoice", source="text", data=data)

    schema_evaluation = report_schema_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    # We expect exactly 1 rule to fail due to the misspelled tag
    assert schema_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the misspelled tag
    assert schema_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(schema_evaluation.violations) == 1

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message
    assert violation.message

    # Check that the location line/column are were the violation is
    assert violation.line == 20
    assert violation.column == 0

def test_schema_tag_order_invalid():
    # Invalidating the date
    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cbc:IssueDate", "", "cbc:DueDate", 1)
    data = invalidate_invoice(data, "tag", "cbc:DueDate", "", "cbc:IssueDate", 2)
    invoice = Invoice(name="My Invoice", source="text", data=data)

    schema_evaluation = report_schema_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert schema_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert schema_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(schema_evaluation.violations) == 1

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message
    assert violation.message

    # Check that the location line/column are were the violation is
    assert violation.line == 5
    assert violation.column == 0

def test_schema_date_type_invalid():
    # Invalidating the date
    data = invalidate_invoice(VALID_INVOICE_TEXT, "content", "cbc:IssueDate", "", "totallyADate", 1)
    invoice = Invoice(name="My Invoice", source="text", data=data)

    schema_evaluation = report_schema_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert schema_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert schema_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(schema_evaluation.violations) == 1

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message
    assert violation.message

    # Check that the location line/column are were the violation is
    assert violation.line == 5
    assert violation.column == 0

def test_schema_tags_revalid():
    # Replacing the tags but making sure they are valid
    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cbc:IssueDate", "", "cbc:CopyIndicator", 1)
    data = invalidate_invoice(data, "content", "cbc:CopyIndicator", "", "true", 1)
    data = invalidate_invoice(data, "tag", "cbc:DueDate", "", "cbc:IssueDate", 1)

    invoice = Invoice(name="My Invoice", source="text", data=data)

    schema_evaluation = report_schema_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    # We expect exactly 0 rule to fail due to the corrections
    assert schema_evaluation.num_rules_failed == 0

    # We expect exactly 0 violation due to the corrections
    assert schema_evaluation.num_errors == 0

    # Thus there should be exactly 0 violation in the violation list
    assert len(schema_evaluation.violations) == 0

def test_schema_tags_multiple_errors_invalid():
    # Replacing with an tag that is valid but expects a different content type.
    # Also expects the following tag to be different
    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cbc:IssueDate", "", "cbc:CopyIndicator", 1)

    invoice = Invoice(name="My Invoice", source="text", data=data)

    schema_evaluation = report_schema_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    # We expect exactly 2 rules to fail due to the invalid tag and content type
    assert schema_evaluation.num_rules_failed == 2

    # We expect exactly 2 violation due to the capitalised tag
    assert schema_evaluation.num_errors == 2

    # Thus there should be exactly 2 violation in the violation list
    assert len(schema_evaluation.violations) == 2

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message
    assert violation.message

    # Check that the location line/column are were the violation is
    assert violation.line == 5
    assert violation.column == 0

    violation = schema_evaluation.violations[1]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message
    assert violation.message

    # Check that the location line/column are were the violation is
    assert violation.line == 6
    assert violation.column == 0
