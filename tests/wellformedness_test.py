from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string

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