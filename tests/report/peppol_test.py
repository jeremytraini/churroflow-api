from tests.server_calls import report_peppol_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import remove_part_of_string

"""
=====================================
/report/peppol/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_peppol_valid_invoice():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    peppol_evaluation = report_peppol_v1(name, format, source, data)
    assert peppol_evaluation["aspect"] == "peppol"

    # We expect many rules to be fired for any invoice
    # This depends on the number of rules in the rule set but should be at least 1
    assert peppol_evaluation["num_rules_fired"] > 0

    # We expect no rules to fail for a valid invoice
    assert peppol_evaluation["num_rules_failed"] == 0

    # We expect no violations for a valid invoice
    assert peppol_evaluation["num_violations"] == 0

    # The violation list should be empty for a valid invoice
    assert len(peppol_evaluation["violations"]) == 0

# Testing that a single rule fails when there is one error in the invoice
def test_peppol_single_volation():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating the ABN
    data = remove_part_of_string(data, 1677, 1679)

    peppol_evaluation = report_peppol_v1(name, format, source, data)

    # We expect exactly 1 rule to fail due to the invalid ABN
    assert peppol_evaluation["num_rules_failed"] == 1

    # We expect exactly 1 violation due to the invalid ABN
    assert peppol_evaluation["num_violations"] == 1

    # Thus there should be exactly 1 violation in the violation list
    assert len(peppol_evaluation["violations"]) == 1

    abn_violation = peppol_evaluation["violations"][0]

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


# Testing that multiple violations are generated when there are multiple errors in the invoice
def test_peppol_multiple_violations_same_rule():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating the 3 ABNs
    data = remove_part_of_string(data, 1677, 1678)
    data = remove_part_of_string(data, 2829, 2830)

    peppol_evaluation = report_peppol_v1(name, format, source, data)

    # We expect exactly 1 distinct rule to fail
    assert peppol_evaluation["num_rules_failed"] == 1

    # We expect exactly 2 violations for each invalid ABN
    assert peppol_evaluation["num_violations"] == 2

    # Thus there should be exactly 2 violations in the violation list
    assert len(peppol_evaluation["violations"]) == 2

    abn_violation1 = peppol_evaluation["violations"][0]
    abn_violation2 = peppol_evaluation["violations"][1]

    # Rule IDs should be the same
    assert abn_violation1["rule_id"] == abn_violation2["rule_id"] == "PEPPOL-COMMON-R050"

    # Locations should be different for each violation
    assert abn_violation1["location"] != abn_violation2["location"]


def test_peppol_multiple_violations_different_rules():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating the 3 ABNs
    data = remove_part_of_string(data, 1677, 1678)
    data = remove_part_of_string(data, 2829, 2830)

    # Invalidating the 2 addresses
    data = remove_part_of_string(data, 2061, 2062)
    data = remove_part_of_string(data, 3508, 3509)

    peppol_evaluation = report_peppol_v1(name, format, source, data)

    # We expect exactly 2 distinct rules to fail
    assert peppol_evaluation["num_rules_failed"] == 2

    # We expect exactly 2 violations for each invalid ABN and 2 violations for each invalid address
    assert peppol_evaluation["num_violations"] == 4

    # Thus there should be exactly 4 violations in the violation list
    assert len(peppol_evaluation["violations"]) == 4

    abn_violation1 = peppol_evaluation["violations"][0]
    abn_violation2 = peppol_evaluation["violations"][1]
    address_violation1 = peppol_evaluation["violations"][2]
    address_violation2 = peppol_evaluation["violations"][3]

    # Rule IDs should be the same for each ABN violation
    assert abn_violation1["rule_id"] == abn_violation2["rule_id"] == "PEPPOL-COMMON-R050"

    # Rule IDs should be the same for each address violation
    assert address_violation1["rule_id"] == address_violation2["rule_id"] == "PEPPOL-COMMON-R010"

    # Locations should be different for each violation
    assert abn_violation1["location"] != abn_violation2["location"]
    assert address_violation1["location"] != address_violation2["location"]


# Testing that a warning doesn't invalidate the report
def test_peppol_warning_doesnt_invalidate_report():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Invalidating the ABN
    data = remove_part_of_string(data, 1677, 1679)

    peppol_evaluation = report_peppol_v1(name, format, source, data)

    # ABN warning rule
    assert peppol_evaluation["violations"][0]["rule_id"] == "PEPPOL-COMMON-R050"

    # Evaluation still valid
    assert peppol_evaluation["is_valid"] == True


# Testing that a fatal error does invalidate the report
def test_peppol_fatal_error_invalidates_report():
    name = "My Invoice"
    format = "xml"
    source = "text"
    data = VALID_INVOICE_TEXT

    # Changing the start date year to 2029
    data = data[:864] + str(2) + data[865:]

    peppol_evaluation = report_peppol_v1(name, format, source, data)

    # "Start date of line period MUST be within invoice period" rule
    assert peppol_evaluation["violations"][0]["rule_id"] == "PEPPOL-EN16931-R110"

    # Evaluation is not valid due to fatal error
    assert peppol_evaluation["is_valid"] == False


