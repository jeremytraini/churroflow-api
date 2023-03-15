from src.type_structure import *
from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, append_to_string, replace_part_of_string
"""
=====================================
/report/wellformedness/v1 TESTS
=====================================
"""
# Wellformedness Testing that the report was generated properly and matches input data
def test_wellformedness_valid_invoice():
    data = VALID_INVOICE_TEXT

    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 0 rule to fail
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect exactly 0 violations
    assert wellformed_evaluation.num_errors == 0

    # Thus there should be exactly 0 violations in the violation list
    assert len(wellformed_evaluation.violations) == 0


def test_wellformedness_case_sensitive_tags_invalid():
    # Invalidating the tags so that only one of the tags is capitalised
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to the capitalised tag
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the capitalised tag
    assert wellformed_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]
    # Check that the violation is flagged as fatal
    assert violation.is_fatal

    # Check that the violation has a non-empty message
    assert violation.message

    # Check that the location line/column are were the violation is
    assert violation.line == 45
    assert violation.column == 44

def test_wellformedness_case_sensitive_tags_valid():
    # Replacing both tags so that they still match
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")
    data = replace_part_of_string(data, 2045, 2047, "id")

    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)
    # We expect 0 rules to fail as it should be wellformed
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect 0 violations
    assert wellformed_evaluation.num_errors == 0

    # There should be no violations in the list
    assert len(wellformed_evaluation.violations) == 0

def test_wellformedness_two_root_elements_invalid():
    data = VALID_INVOICE_TEXT
    data = append_to_string(data, """<root><h>Second root at the end</h></root>""")
    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to having two root elements
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the two root elements
    assert wellformed_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message
    assert violation.message

def test_wellformedness_no_closing_tag_invalid():
    data = VALID_INVOICE_TEXT
    data = remove_part_of_string(data, 11530, 11540)
    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to having no closing tag for root element
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the missing closing tag
    assert wellformed_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message
    assert violation.message

# Tag opens in a nest but closes outside
def test_wellformedness_wrong_nesting_invalid():
    data = VALID_INVOICE_TEXT
    data = remove_part_of_string(data, 11512, 11530)
    data = append_to_string(data, """</cac:InvoiceLine>""")
    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the missing closing tag in the nest
    assert wellformed_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.rule_id == "wellformedness" # need to find correct rule_id
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message
    assert violation.message

def test_wellformedness_valid_version_number_error():
    data = VALID_INVOICE_TEXT

    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformedness_evaluation = report_wellformedness_v1(invoice)
    wellformedness_evaluation = Evaluation(**wellformedness_evaluation)
    
    assert data[15] == '1' or data[15] == '2'

    # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
    assert wellformedness_evaluation.num_rules_failed == 0

    # We expect exactly 1 violation due to the missing closing tag in the nest
    assert wellformedness_evaluation.num_errors == 0

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformedness_evaluation.violations) == 0



def test_wellformedness_invalid_version_number_error():
    data = VALID_INVOICE_TEXT
    data = replace_part_of_string(data, 15, 16, '5')

    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformedness_evaluation = report_wellformedness_v1(invoice)
    wellformedness_evaluation = Evaluation(**wellformedness_evaluation)
    
    assert data[15] == '5'

    # We expect exactly 1 rule to fail due to having no closing tag in the corresponding nest
    assert wellformedness_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the missing closing tag in the nest
    assert wellformedness_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformedness_evaluation.violations) == 1

    violation = wellformedness_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.rule_id == "wellformedness" # need to find correct rule_id
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message
    assert violation.message

def test_wellformedness_no_escape_for_special_char_invalid():
    data = VALID_INVOICE_TEXT
    data = replace_part_of_string(data, 694, 695, "<")
    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 1 rule to fail due to not escaping a special character
    assert wellformed_evaluation.num_rules_failed == 1

    # We expect exactly 1 violation due to the special character
    assert wellformed_evaluation.num_errors == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformed_evaluation.violations) == 1

    violation = wellformed_evaluation.violations[0]

    # Check that the violation is for the correct rule and is flagged as fatal
    assert violation.rule_id == "wellformedness" # need to find correct rule_id
    assert violation.is_fatal == True

    # Check that the violation has a non-empty message
    assert violation.message
    
    # Check that the location line/column are were the violation is
    assert violation.line == 11
    assert violation.column == 25

def test_wellformedness_escape_for_special_char_valid():
    data = VALID_INVOICE_TEXT
    data = replace_part_of_string(data, 694, 695, "&lt;")
    invoice = TextInvoice(name="My Invoice", source="text", text=data)

    wellformed_evaluation = report_wellformedness_v1(invoice)
    wellformed_evaluation = Evaluation(**wellformed_evaluation)

    # We expect exactly 0 rules to fail due to escaping the special character
    assert wellformed_evaluation.num_rules_failed == 0

    # We expect exactly 0 violation due to escaping the special character
    assert wellformed_evaluation.num_errors == 0

    # Thus there should be exactly 0 violation in the violation list
    assert len(wellformed_evaluation.violations) == 0
