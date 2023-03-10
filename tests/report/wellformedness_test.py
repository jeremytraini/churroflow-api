from src.types import *
import pydantic
from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, append_to_string, replace_part_of_string, invalidate_invoice

"""
=====================================
/report/wellformedness/v1 TESTS
=====================================
"""
# Wellformedness Testing that the report was generated properly and matches input data
def test_wellformed_valid_invoice():
    data = VALID_INVOICE_TEXT

    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 0 rule to fail
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect exactly 0 violations
    assert wellformed_evaluation.num_violations == 0

    # Thus there should be exactly 0 violations in the violation list
    assert len(wellformed_evaluation.violations) == 0


def test_wellformed_case_sensitive_tags_invalid():
    # Invalidating the tags so that only one of the tags is capitalised
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

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

    # Check that the violation has a non-empty message and suggestion
    assert violation.message
    assert violation.suggestion

    assert violation.location.type == "line"

    # Check that the location line/column are were the violation is
    assert violation.location.line == 45
    assert violation.location.column == 44

def test_wellformed_case_sensitive_tags_valid():
    # Replacing both tags so that they still match
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")
    data = replace_part_of_string(data, 2045, 2047, "id")

    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)
    # We expect 0 rules to fail as it should be wellformed
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect 0 violations
    assert wellformed_evaluation.num_violations == 0

    # There should be no violations in the list
    assert len(wellformed_evaluation.violations) == 0

def test_two_root_elements_invalid():
    data = VALID_INVOICE_TEXT
    data = append_to_string(data, """<root><h>Second root at the end</h></root>""")
    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to having two root elements
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the two root elements
    assert wellformed_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message and suggestion
    assert violation.message
    assert violation.suggestion

def test_no_closing_tag_invalid():
    data = VALID_INVOICE_TEXT
    data = remove_part_of_string(data, 11530, 11540)
    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to having no closing tag for root element
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the missing closing tag
    assert wellformed_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message and suggestion
    assert violation.message
    assert violation.suggestion

# Tag opens in a nest but closes outside
def test_wrong_nesting_invalid():
    data = VALID_INVOICE_TEXT
    data = remove_part_of_string(data, 11512, 11530)
    data = append_to_string(data, """</cac:InvoiceLine>""")
    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the missing closing tag in the nest
    assert wellformed_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.rule_id == "wellformedness" # need to find correct rule_id
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message and suggestion
    assert violation.message
    assert violation.suggestion


# # Testing that a single rule fails when there is one attribute error in the invoice
# def test_wellformed_single_violation():
#     data = VALID_INVOICE_TEXT

#     # Invalidating the currency code by replacing AUD
#     data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'HELLO', 1)

#     invoice = Invoice(name="My Invoice", source="text", data=data)

#     wellformedness_evaluation = report_wellformedness_v1(invoice)
#     wellformedness_evaluation = Evaluation(**wellformedness_evaluation)

#     # We expect exactly 1 rule to fail due to the invalid currency code
#     assert wellformedness_evaluation.num_rules_failed == 1

#     # We expect exactly 1 violation due to the invalid currency code
#     assert wellformedness_evaluation.num_violations == 1

#     # Thus there should be exactly 1 violation in the violation list
#     assert len(wellformedness_evaluation.violations) == 1

#     code_violation = wellformedness_evaluation.violations[0]

#     # From 'A-NZ_Invoice_Extension_v1.0.8.docx' file:
#     # BR-CL-04 | [BR-CL-04]-Invoice currency code MUST be coded using ISO code list 4217 alpha-3 | Same | fatal

#     # Check that the violation is for the correct rule and is flagged as fatal
#     assert code_violation.rule_id == "BR-CL-03"
#     assert code_violation.is_fatal == True

#     # Check that the violation has a non-empty message, test and suggestion
#     assert code_violation.message
#     assert code_violation.test
#     assert code_violation.suggestion

#     assert code_violation.location.type == "xpath"

#     # Check that the location xpath is not empty
#     assert code_violation.location.xpath

# # Testing that a single rule fails when there is multiple attribute error in the invoice
# def test_wellformed_multiple_violations_different_rules():
#     data = VALID_INVOICE_TEXT

#     # Invalidating 2 currency codes
#     data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'HELLO', 1)
#     data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'HELLO', 2)

#     # Invalidating the 2 Country/IdentificationCode
#     data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'HELLO', 1)
#     data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'HELLO', 2)

#     invoice = Invoice(name="My Invoice", source="text", data=data)

#     wellformedness_evaluation = report_wellformedness_v1(invoice)
#     wellformedness_evaluation = Evaluation(**wellformedness_evaluation)

#     # We expect exactly 2 distinct rules to fail
#     assert wellformedness_evaluation.num_rules_failed == 2

#     # We expect exactly 2 violations for each invalid currency code and 2 violations for each invalid address
#     assert wellformedness_evaluation.num_violations == 4

#     # Thus there should be exactly 4 violations in the violation list
#     assert len(wellformedness_evaluation.violations) == 4

#     code_violation1 = wellformedness_evaluation.violations[0]
#     code_violation2 = wellformedness_evaluation.violations[1]
#     id_code_violation1 = wellformedness_evaluation.violations[2]
#     id_code_violation2 = wellformedness_evaluation.violations[3]

#     # Rule IDs should be the same for each currency code violation
#     assert code_violation1.rule_id == code_violation2.rule_id == "BR-CL-14"

#     # Rule IDs should be the same for each IdentificationCode violation
#     assert id_code_violation1.rule_id == id_code_violation2.rule_id == "BR-CL-03"

#     # Locations should be different for each violation
#     assert code_violation1.location != code_violation2.location
#     assert id_code_violation1.location != id_code_violation2.location

def test_wellformedness_valid_version_number_error():
    data = VALID_INVOICE_TEXT

    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformedness_evaluation = report_wellformedness_v1(invoice)
    wellformedness_evaluation = Evaluation(**wellformedness_evaluation)
    print(wellformedness_evaluation)
    assert wellformedness_evaluation.aspect == "wellformedness"
    assert data[15] == '1' or data[15] == '2'

    # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
    assert wellformedness_evaluation.num_rules_failed == 0

    # We expect exactly 1 violation due to the missing closing tag in the nest
    assert wellformedness_evaluation.num_violations == 0

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformedness_evaluation.violations) == 0



def test_wellformedness_invalid_version_number_error():
    data = VALID_INVOICE_TEXT
    data = replace_part_of_string(data, 15, 16, '5')

    print(data[15:17])
    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformedness_evaluation = report_wellformedness_v1(invoice)
    wellformedness_evaluation = Evaluation(**wellformedness_evaluation)
    print(wellformedness_evaluation)
    assert wellformedness_evaluation.aspect == "wellformedness"
    assert data[15] == '5'

    # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
    assert wellformedness_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the missing closing tag in the nest
    assert wellformedness_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformedness_evaluation.violations) == 1

    violation = wellformedness_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.rule_id == "wellformedness" # need to find correct rule_id
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message and suggestion
    assert violation.message
    assert violation.suggestion


# def test_escape_special_char_valid():
#     data = VALID_INVOICE_TEXT
#     data = replace_part_of_string(data, 499, 503, "&lt;")
#     invoice = Invoice(name="My Invoice", source="text", data=data)

#     wellformed_evaluation = report_wellformedness_v1(invoice)
#     wellformed_evaluation = Evaluation(**wellformed_evaluation)

#     # We expect exactly 0 rules to fail since the special character was escaped
#     assert wellformed_evaluation.num_rules_failed == 0

#     # We expect exactly 0 violations
#     assert wellformed_evaluation.num_violations == 0

#     # Thus there should've be any violation
#     assert len(wellformed_evaluation.violations) == 0


def test_no_escape_for_special_char_invalid():
    data = VALID_INVOICE_TEXT
    data = replace_part_of_string(data, 499, 500, "<")
    invoice = Invoice(name="My Invoice", source="text", data=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to not escaping a special character
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the special character
    assert wellformed_evaluation.num_violations == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.rule_id == "wellformedness" # need to find correct rule_id
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message and suggestion
    assert violation.message
    assert violation.suggestion

