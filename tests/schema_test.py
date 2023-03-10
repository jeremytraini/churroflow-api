from src.types import Invoice, Evaluation
from tests.server_calls import report_schemavalid_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import *

"""
=====================================
/report/schemavalid/v1 TESTS
=====================================
"""
def test_UBL_VersionID_specified_twice_invalid():
    # Invalidating the date
    data = squeeze_text_inbetween(VALID_INVOICE_TEXT, 530, 532, "20")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    schema_evaluation = report_schemavalid_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    assert schema_evaluation.aspect == "schema"

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert schema_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert schema_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(schema_evaluation.violations) == 1

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message, test and suggestion
    assert violation.message
    assert violation.test
    assert violation.suggestion
    
    assert violation.location.type == "line"

    # Check that the location line/column are were the violation is
    assert violation.location.line == 1
    assert violation.location.column == 555

def test_schema_currency_id_invalid():
    # Invalidating the date
    data = insert_into_string(VALID_INVOICE_TEXT, 6200, "D")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    schema_evaluation = report_schemavalid_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    assert schema_evaluation.aspect == "schema"

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert schema_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert schema_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(schema_evaluation.violations) == 1

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message, test and suggestion
    assert violation.message
    assert violation.test
    assert violation.suggestion
    
    assert violation.location.type == "line"

    # Check that the location line/column are were the violation is
    assert violation.location.line == 1
    assert violation.location.column == 555

def test_schema_percent_invalid():
    # Invalidating the date
    data = insert_into_string(VALID_INVOICE_TEXT, 6316, "0")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    schema_evaluation = report_schemavalid_v1(invoice)
    schema_evaluation = Evaluation(**schema_evaluation)

    assert schema_evaluation.aspect == "schema"

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert schema_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert schema_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(schema_evaluation.violations) == 1

    violation = schema_evaluation.violations[0]

    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message, test and suggestion
    assert violation.message
    assert violation.test
    assert violation.suggestion
    
    assert violation.location.type == "line"

    # Check that the location line/column are were the violation is
    assert violation.location.line == 1
    assert violation.location.column == 555