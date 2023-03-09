from src.types import *
from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, append_to_string, replace_part_of_string

"""
=====================================
/report/wellformedness/v1 TESTS - (7 CASES TO BE TESTED)
=====================================
"""
# Wellformedness Testing that the report was generated properly and matches input data
def test_wellformed_valid_invoice():
    data = VALID_INVOICE_TEXT

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 0 rule to fail
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect exactly 0 violations
    assert wellformed_evaluation.num_violations == 0

    # Thus there should be exactly 0 violations in the violation list
    assert len(wellformed_evaluation.violations) == 0


# def test_wellformed_case_sensitive_tags_invalid():
#     # Invalidating the tags so that only one of the tags is capitalised
#     data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

#     invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)
    
#     assert wellformed_evaluation.aspect == "wellformedness"

#     # We expect exactly 1 rule to fail due to the capitalised tag
#     assert wellformed_evaluation.num_rules_failed == 1

#     # We expect exactly 1 violation due to the capitalised tag
#     assert wellformed_evaluation.num_violations == 1

#     # Thus there should be exactly 1 violation in the violation list
#     assert len(wellformed_evaluation.violations) == 1

#     violation = wellformed_evaluation.violations[0]
#     # Check that the violation is flagged as fatal
#     assert violation.is_fatal

#     # Check that the violation has a non-empty message, test and suggestion
#     assert violation.message
#     assert violation.test
#     assert violation.suggestion
    
#     assert violation.location.type == "line"

#     # Check that the location line/column are were the violation is
#     assert violation.location.line == 1
#     assert violation.location.column == 2256

def test_wellformed_case_sensitive_tags_valid():
    # Replacing both tags so that they still match
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")
    data = replace_part_of_string(data, 2045, 2047, "id")

    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)
    # We expect 0 rules to fail as it should be wellformed
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect 0 violations
    assert wellformed_evaluation.num_violations == 0

    # There should be no violations in the list
    assert len(wellformed_evaluation.violations) == 0

# def test_two_root_elements_invalid():
#     data = VALID_INVOICE_TEXT
#     data = append_to_string(data, """<root><h>Second root at the end</h></root>""")
#     invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)

#     # We expect exactly 1 rule to fail due to having two root elements
#     assert wellformed_evaluation.num_rules_failed == 1

#     # We expect exactly 1 violation due to the two root elements
#     assert wellformed_evaluation.num_violations == 1

#     # Thus there should be exactly 1 violation in the violation list
#     assert len(wellformed_evaluation.violations) == 1

#     violation = wellformed_evaluation.violations[0]

#     # Check that the violation is for the correct rule and is flagged as fatal
#     assert violation.rule_id == "errorName" # need to find correct rule_id
#     assert violation.is_fatal == True

#     # Check that the violation has a non-empty message, test and suggestion
#     assert violation.message
#     assert violation.test
#     assert violation.suggestion

# def test_no_closing_tag_invalid():
#     data = VALID_INVOICE_TEXT
#     data = remove_part_of_string(data, 11530, 11540)
#     invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)

#     # We expect exactly 1 rule to fail due to having no closing tag for root element
#     assert wellformed_evaluation.num_rules_failed == 1

#     # We expect exactly 1 violation due to the missing closing tag
#     assert wellformed_evaluation.num_violations == 1

#     # Thus there should be exactly 1 violation in the violation list
#     assert len(wellformed_evaluation.violations) == 1

#     violation = wellformed_evaluation.violations[0]

#     # Check that the violation is for the correct rule and is flagged as fatal
#     assert violation.rule_id == "errorName" # need to find correct rule_id
#     assert violation.is_fatal == True

#     # Check that the violation has a non-empty message, test and suggestion
#     assert violation.message
#     assert violation.test
#     assert violation.suggestion


# Tag opens in a nest but closes outside
# def test_wrong_nesting_invalid():
#     data = VALID_INVOICE_TEXT
#     data = remove_part_of_string(data, 11512, 11530)
#     data = append_to_string(data, """</cac:InvoiceLine>""") 
#     invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)

#     # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
#     assert wellformed_evaluation.num_rules_failed == 1

#     # We expect exactly 1 violation due to the missing closing tag in the nest
#     assert wellformed_evaluation.num_violations == 1

#     # Thus there should be exactly 1 violation in the violation list
#     assert len(wellformed_evaluation.violations) == 1

#     violation = wellformed_evaluation.violations[0]

#     # Check that the violation is for the correct rule and is flagged as fatal
#     assert violation.rule_id == "errorName" # need to find correct rule_id
#     assert violation.is_fatal == True

#     # Check that the violation has a non-empty message, test and suggestion
#     assert violation.message
#     assert violation.test
#     assert violation.suggestion


# def test_no_escape_for_special_char_invalid():
#     data = VALID_INVOICE_TEXT
#     data = replace_part_of_string(data, 499, 500, "<")
#     invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)

#     # We expect exactly 1 rule to fail due to not escaping a special character
#     assert wellformed_evaluation.num_rules_failed == 1

#     # We expect exactly 1 violation due to the special character
#     assert wellformed_evaluation.num_violations == 1

#     # Thus there should be exactly 1 violation in the violation list
#     assert len(wellformed_evaluation.violations) == 1

#     violation = wellformed_evaluation.violations[0]

#     # Check that the violation is for the correct rule and is flagged as fatal
#     assert violation.rule_id == "errorName" # need to find correct rule_id
#     assert violation.is_fatal == True

#     # Check that the violation has a non-empty message, test and suggestion
#     assert violation.message
#     assert violation.test
#     assert violation.suggestion

def test_escape_special_char_valid():
    data = VALID_INVOICE_TEXT
    data = replace_part_of_string(data, 499, 503, "&lt;")
    invoice = Invoice(name="My Invoice", format="XML", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 0 rules to fail since the special character was escaped
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect exactly 0 violations
    assert wellformed_evaluation.num_violations == 0

    # Thus there should've be any violation
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
