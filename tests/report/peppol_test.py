from src.type_structure import *
from tests.server_calls import report_peppol_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/report/peppol/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_peppol_valid_invoice():
    data = VALID_INVOICE_TEXT
    
    invoice = Invoice(name="My Invoice", source="text", data=data)
    
    peppol_evaluation = report_peppol_v1(invoice)
    peppol_evaluation = Evaluation(**peppol_evaluation)
    
    assert peppol_evaluation.aspect == "peppol"
    
    # We expect no rules to fail for a valid invoice
    assert peppol_evaluation.num_rules_failed == 0
    
    # We expect no violations for a valid invoice
    assert peppol_evaluation.num_violations == 0
    
    # The violation list should be empty for a valid invoice
    assert len(peppol_evaluation.violations) == 0

# Testing that a single rule fails when there is one error in the invoice
def test_peppol_single_volation():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the ABN, changing the content of the ABN
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
    
    invoice = Invoice(name="My Invoice", source="text", data=data)
    
    peppol_evaluation = report_peppol_v1(invoice)
    peppol_evaluation = Evaluation(**peppol_evaluation)
    
    # We expect exactly 1 rule to fail due to the invalid ABN
    assert peppol_evaluation.num_rules_failed == 1
    
    # We expect exactly 1 violation due to the invalid ABN
    assert peppol_evaluation.num_violations == 1
    
    # Thus there should be exactly 1 violation in the violation list
    assert len(peppol_evaluation.violations) == 1
    
    abn_violation = peppol_evaluation.violations[0]
    
    # From 'A-NZ_Invoice_Extension_v1.0.8.docx' file:
    # PEPPOL-COMMON-R050 | Australian Business Number (ABN) MUST be stated in the correct format. | Same | warning
    
    # Check that the violation is for the correct rule and is flagged as fatal
    assert abn_violation.rule_id == "PEPPOL-COMMON-R050"
    assert abn_violation.is_fatal == False
    
    # Check that the violation has a non-empty message, test and suggestion
    assert abn_violation.message
    assert abn_violation.test
    assert abn_violation.suggestion
    
    # Check that the location xpath is not empty
    assert abn_violation.xpath


# Testing that multiple violations are generated when there are multiple errors in the invoice
def test_peppol_multiple_violations_same_rule():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the 2 ABNs
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 1', 1)
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 2', 2)
    
    invoice = Invoice(name="My Invoice", source="text", data=data)
    
    peppol_evaluation = report_peppol_v1(invoice)
    peppol_evaluation = Evaluation(**peppol_evaluation)
    
    # We expect exactly 1 distinct rule to fail
    assert peppol_evaluation.num_rules_failed == 1
    
    # We expect exactly 2 violations for each invalid ABN
    assert peppol_evaluation.num_violations == 2
    
    # Thus there should be exactly 2 violations in the violation list
    assert len(peppol_evaluation.violations) == 2
    
    abn_violation1 = peppol_evaluation.violations[0]
    abn_violation2 = peppol_evaluation.violations[1]
    
    # Rule IDs should be the same
    assert abn_violation1.rule_id == abn_violation2.rule_id == "PEPPOL-COMMON-R050"
    
    # Locations should be different for each violation
    assert abn_violation1.xpath != abn_violation2.xpath


def test_peppol_multiple_violations_different_rules():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the 2 ABNs
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 1', 1)
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 2', 2)
    
    # Invalidating the 2 addresses
    data = invalidate_invoice(data, 'content', 'cbc:IssueDate', '', 'bad-date', 1)
    data = invalidate_invoice(data, 'content', 'cbc:IssueDate', '', 'bad-date', 2)
    
    invoice = Invoice(name="My Invoice", source="text", data=data)
    
    peppol_evaluation = report_peppol_v1(invoice)
    peppol_evaluation = Evaluation(**peppol_evaluation)
    
    # We expect exactly 2 distinct rules to fail
    assert peppol_evaluation.num_rules_failed == 2
    
    # We expect exactly 2 violations for each invalid ABN and 2 violations for each invalid address
    assert peppol_evaluation.num_violations == 4
    
    # Thus there should be exactly 4 violations in the violation list
    assert len(peppol_evaluation.violations) == 4
    
    abn_violation1 = peppol_evaluation.violations[0]
    abn_violation2 = peppol_evaluation.violations[1]
    address_violation1 = peppol_evaluation.violations[2]
    address_violation2 = peppol_evaluation.violations[3]
    
    # Rule IDs should be the same for each ABN violation
    assert abn_violation1.rule_id == abn_violation2.rule_id == "PEPPOL-COMMON-R050"
    
    # Rule IDs should be the same for each address violation
    assert address_violation1.rule_id == address_violation2.rule_id == "PEPPOL-EN16931-F001"
    
    # Locations should be different for each violation
    assert abn_violation1.xpath != abn_violation2.xpath
    assert address_violation1.xpath != address_violation2.xpath


# Testing that a warning doesn't invalidate the report
def test_peppol_warning_doesnt_invalidate_report():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the ABN
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 1', 1)
    
    invoice = Invoice(name="My Invoice", source="text", data=data)
    
    peppol_evaluation = report_peppol_v1(invoice)
    peppol_evaluation = Evaluation(**peppol_evaluation)
    
    # ABN warning rule
    assert peppol_evaluation.violations[0].rule_id == "PEPPOL-COMMON-R050"
    
    # Evaluation still valid
    assert peppol_evaluation.is_valid == True

    
# Testing that a fatal error does invalidate the report
def test_peppol_fatal_error_invalidates_report():
    data = VALID_INVOICE_TEXT
    
    # Changing the start date year to 2029
    data = invalidate_invoice(data, 'content', 'cbc:IssueDate', '', 'bad-date', 1)
    
    invoice = Invoice(name="My Invoice", source="text", data=data)
    
    peppol_evaluation = report_peppol_v1(invoice)
    peppol_evaluation = Evaluation(**peppol_evaluation)
    
    # "Start date of line period MUST be within invoice period" rule
    assert peppol_evaluation.violations[0].rule_id == "PEPPOL-EN16931-F001"
    
    # Evaluation is not valid due to fatal error
    assert peppol_evaluation.is_valid == False
