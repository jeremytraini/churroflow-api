from src.types import Invoice, LocationLine, LocationXpath
from tests.server_calls import report_schemavalid_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, replace_part_of_string
from src.report import report_schemavalid_v1 as schema_function_direct

"""
=====================================
/report/schemavalid/v1 TESTS
=====================================
"""
def test_schema_invalid():
    # Invalidating the tags so that only one of the tags is capitalised
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2256, 2258, "id")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    schema_evaluation = report_schemavalid_v1(invoice)

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

    location = LocationLine(violation.location)
    
    assert location.type == "line"

    # Check that the location line/column are were the violation is
    assert location.line == 1
    assert location.column == 2256

def test_schema_functional():
    # Invalidating the tags so that only one of the tags is capitalised
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2256, 2258, "id")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    schema_evaluation = schema_function_direct(invoice)

    assert schema_evaluation.aspect == "schema"
