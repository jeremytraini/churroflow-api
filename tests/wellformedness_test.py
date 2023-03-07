from src.types import Invoice, LocationLine, LocationXpath
from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, replace_part_of_string

"""
=====================================
/report/wellformedness/v1 TESTS - (7 CASES TO BE TESTED)
=====================================
"""
# Wellformedness Testing that the report was generated properly and matches input data
def test_wellformed_valid_invoice():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating the ABN
    data = remove_part_of_string(data, 11554, 11555)

    wellformed_evaluation = report_wellformedness_v1(name, format, source, data)

    # We expect exactly 1 rule to fail due to the invalid ABN
    assert wellformed_evaluation["num_rules_failed"] == 1

    # We expect exactly 1 violation due to the invalid ABN
    assert wellformed_evaluation["num_violations"] == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation["violations"]) == 1

    abn_violation = wellformed_evaluation["violations"][0]

    # From 'A-NZ_Invoice_Extension_v1.0.8.docx' file:
    # PEPPOL-COMMON-R050 | Australian Business Number (ABN) MUST be stated in the correct format. | Same | warning

    # Check that the violation is for the correct rule and is flagged as fatal
    assert abn_violation["rule_id"] == "PEPPOL-COMMON-R050"
    assert abn_violation["is_fatal"] == True

    # Check that the violation has a non-empty message, test and suggestion
    assert abn_violation["message"]
    assert abn_violation["test"]
    assert abn_violation["suggestion"]

    assert abn_violation["location"]["type"] == "xpath"

    # Check that the location xpath is not empty
    assert abn_violation["location"]["xpath"]

def test_wellformed_case_sensitive_tags_invalid():
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

def test_wellformed_case_sensitive_tags_valid():
    # Replacing both tags so that they still match
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2244, 2246, "id")
    data = replace_part_of_string(data, 2256, 2258, "id")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)

    # We expect 0 rules to fail as it should be wellformed
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect 0 violations
    assert wellformed_evaluation.num_violations == 0

    # There should be no violations in the list
    assert len(wellformed_evaluation.violations) == 0

# Root element - closing tag + nesting - Ricardo
# Attributes in quotes - currencyID="AUD" - currency + schemeID="HWB" - Ahona - remove the quotes and test
# Case sensitive - Mohamad
# declaration at the beginning- version has to be less than 2.1 - Ahona
# escape xml special characters - Ricardo
# <Invoice>\n\Hello World < <Invoice>

# - Check failing and success case
# do them all separately
# DO failing and success test in each case

# 5 errors
# 1 2 3 4 5
# 1 st error + terminates