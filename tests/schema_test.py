from src.types import Invoice, LocationLine, LocationXpath
from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, replace_part_of_string

"""
=====================================
/report/schemavalid/v1 TESTS
=====================================
"""
def test_schema_invalid():
    # Invalidating the tags so that only one of the tags is capitalised
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2256, 2258, "id")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)

    assert wellformed_evaluation.aspect == "wellformedness"

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert wellformed_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

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