from tests.server_calls import report_wellformedness_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string, invalidate_invoice
"""
=====================================
/report/wellformedness/v1 TESTS
=====================================
"""
# Testing that a single rule fails when there is one attribute error in the invoice
def test_wellformed_single_violation():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating the currency code by replacing AUD
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'HELLO', 1)

    wellformedness_evaluation = report_wellformedness_v1(name, format, source, data)

    # We expect exactly 1 rule to fail due to the invalid currency code
    assert wellformedness_evaluation["num_rules_failed"] == 1

    # We expect exactly 1 violation due to the invalid currency code
    assert wellformedness_evaluation["num_violations"] == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(wellformedness_evaluation["violations"]) == 1

    code_violation = wellformedness_evaluation["violations"][0]

    # From 'A-NZ_Invoice_Extension_v1.0.8.docx' file:
    # BR-CL-04 | [BR-CL-04]-Invoice currency code MUST be coded using ISO code list 4217 alpha-3 | Same | fatal

    # Check that the violation is for the correct rule and is flagged as fatal
    assert code_violation["rule_id"] == "BR-CL-03"
    assert code_violation["is_fatal"] == True

    # Check that the violation has a non-empty message, test and suggestion
    assert code_violation["message"]
    assert code_violation["test"]
    assert code_violation["suggestion"]

    assert code_violation["location"]["type"] == "xpath"

    # Check that the location xpath is not empty
    assert code_violation["location"]["xpath"]

# Testing that a single rule fails when there is multiple attribute error in the invoice
def test_wellformed_multiple_violations_different_rules():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating 2 currency codes
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'HELLO', 1)
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'HELLO', 2)

    # Invalidating the 2 Country/IdentificationCode
    data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'HELLO', 1)
    data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'HELLO', 2)

    wellformedness_evaluation = report_wellformedness_v1(name, format, source, data)

    # We expect exactly 2 distinct rules to fail
    assert wellformedness_evaluation["num_rules_failed"] == 2

    # We expect exactly 2 violations for each invalid currency code and 2 violations for each invalid address
    assert wellformedness_evaluation["num_violations"] == 4

    # Thus there should be exactly 4 violations in the violation list
    assert len(wellformedness_evaluation["violations"]) == 4

    code_violation1 = wellformedness_evaluation["violations"][0]
    code_violation2 = wellformedness_evaluation["violations"][1]
    id_code_violation1 = wellformedness_evaluation["violations"][2]
    id_code_violation2 = wellformedness_evaluation["violations"][3]

    # Rule IDs should be the same for each currency code violation
    assert code_violation1["rule_id"] == code_violation2["rule_id"] == "BR-CL-14"

    # Rule IDs should be the same for each IdentificationCode violation
    assert id_code_violation1["rule_id"] == id_code_violation2["rule_id"] == "BR-CL-03"

    # Locations should be different for each violation
    assert code_violation1["location"] != code_violation2["location"]
    assert id_code_violation1["location"] != id_code_violation2["location"]

def test_wellformedness_version_number_error():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    wellformedness_evaluation = report_wellformedness_v1(name, format, source, data)
    print(wellformedness_evaluation)
    assert wellformedness_evaluation["aspect"] == "wellformedness"
    assert data[16] == "1" or data[16] == "2"

    # We expect many rules to be fired for any invoice
    # This depends on the number of rules in the rule set but should be at least 1
    assert wellformedness_evaluation["num_rules_fired"] > 0

    # We expect no rules to fail for a valid invoice
    assert wellformedness_evaluation["num_rules_failed"] == 0

    # We expect no violations for a valid invoice
    assert wellformedness_evaluation["num_violations"] == 0

    # The violation list should be empty for a valid invoice
    assert len(wellformedness_evaluation["violations"]) == 0

# def test_wellformedness():