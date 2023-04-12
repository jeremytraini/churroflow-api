from src.type_structure import *
from tests.server_calls import report_syntax_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, replace_part_of_string, clear_database

"""
=====================================
/report/syntax/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_syntax_valid_invoice():
    data = VALID_INVOICE_TEXT
    
    invoice = TextInvoice(name="My Invoice", text=data)

    syntax_evaluation = report_syntax_v1(invoice)
    syntax_evaluation = Evaluation(**syntax_evaluation)
    
    # We expect no rules to fail for a valid invoice
    assert syntax_evaluation.num_rules_failed == 0
    
    # We expect no violations for a valid invoice
    assert syntax_evaluation.num_errors == 0
    
    # The violation list should be empty for a valid invoice
    assert len(syntax_evaluation.violations) == 0

# Testing that a single rule fails when there is one error in the invoice
def test_syntax_single_violation():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the currency code
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    
    invoice = TextInvoice(name="My Invoice", text=data)

    syntax_evaluation = report_syntax_v1(invoice)
    syntax_evaluation = Evaluation(**syntax_evaluation)
    
    # We expect exactly 1 rule to fail due to the invalid currency code
    assert syntax_evaluation.num_rules_failed == 1
    
    # We expect exactly 1 violation due to the invalid currency code
    assert syntax_evaluation.num_errors == 1
    
    # Thus there should be exactly 1 violation in the violation list
    assert len(syntax_evaluation.violations) == 1
    
    code_violation = syntax_evaluation.violations[0]
    
    # From 'A-NZ_Invoice_Extension_v1.0.8.docx' file:
    # BR-CL-04 | [BR-CL-04]-Invoice currency code MUST be coded using ISO code list 4217 alpha-3 | Same | fatal
    
    # Check that the violation is for the correct rule and is flagged as fatal
    assert code_violation.rule_id == "BR-CL-03"
    assert code_violation.is_fatal == True
    
    # Check that the violation has a non-empty message, test and suggestion
    assert code_violation.message
    assert code_violation.test
    
    # Check that the location xpath is not empty
    assert code_violation.xpath


# Testing that multiple violations are generated when there are multiple errors in the invoice
def test_syntax_multiple_violations_same_rule():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the 2 currency codes
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 2)
    
    invoice = TextInvoice(name="My Invoice", text=data)

    syntax_evaluation = report_syntax_v1(invoice)
    syntax_evaluation = Evaluation(**syntax_evaluation)
    
    # We expect exactly 1 distinct rule to fail
    assert syntax_evaluation.num_rules_failed == 1
    
    # We expect exactly 2 violations for each invalid currency code
    assert syntax_evaluation.num_errors == 2
    
    # Thus there should be exactly 2 violations in the violation list
    assert len(syntax_evaluation.violations) == 2
    
    code_violation1 = syntax_evaluation.violations[0]
    code_violation2 = syntax_evaluation.violations[1]
    
    # Rule IDs should be the same
    assert code_violation1.rule_id == code_violation2.rule_id == "BR-CL-03"
    
    # Locations should be different for each violation
    assert code_violation1.xpath != code_violation2.xpath


def test_syntax_multiple_violations_different_rules():
    data = VALID_INVOICE_TEXT
    
    # Invalidating 2 currency codes
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 2)
    
    # Invalidating the 2 Country/IdentificationCode
    data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'TEST', 1)
    data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'TEST', 2)
    
    invoice = TextInvoice(name="My Invoice", text=data)

    syntax_evaluation = report_syntax_v1(invoice)
    syntax_evaluation = Evaluation(**syntax_evaluation)
    
    # We expect exactly 2 distinct rules to fail
    assert syntax_evaluation.num_rules_failed == 2
    
    # We expect exactly 2 violations for each invalid currency code and 2 violations for each invalid address
    assert syntax_evaluation.num_errors == 4
    
    # Thus there should be exactly 4 violations in the violation list
    assert len(syntax_evaluation.violations) == 4
    
    code_violation1 = syntax_evaluation.violations[0]
    code_violation2 = syntax_evaluation.violations[1]
    id_code_violation1 = syntax_evaluation.violations[2]
    id_code_violation2 = syntax_evaluation.violations[3]
    
    # Rule IDs should be the same for each currency code violation
    assert code_violation1.rule_id == code_violation2.rule_id == "BR-CL-14"
    
    # Rule IDs should be the same for each IdentificationCode violation
    assert id_code_violation1.rule_id == id_code_violation2.rule_id == "BR-CL-03"
    
    # Locations should be different for each violation
    assert code_violation1.xpath != code_violation2.xpath
    assert id_code_violation1.xpath != id_code_violation2.xpath


# Testing that a warning doesn't invalidate the report
def test_syntax_warning_doesnt_invalidate_report():
    data = VALID_INVOICE_TEXT
    
    # Adding 1 'cbc:ProfileExecutionID' tag
    # Violates [UBL-CR-003]-A UBL invoice should not include the ProfileExecutionID
    data = invalidate_invoice(data, 'tag', 'cbc:Note', '', 'cbc:ProfileExecutionID', 1)
    
    invoice = TextInvoice(name="My Invoice", text=data)

    syntax_evaluation = report_syntax_v1(invoice)
    syntax_evaluation = Evaluation(**syntax_evaluation)
    
    # Currency code warning rule
    assert syntax_evaluation.violations[0].rule_id == "UBL-CR-003"
    
    # Evaluation still valid
    assert syntax_evaluation.is_valid == True

    
# Testing that a fatal error does invalidate the report
def test_syntax_fatal_error_invalidates_report():
    data = VALID_INVOICE_TEXT
    
    # Adding "D" to the currency code to make it invalid
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    
    invoice = TextInvoice(name="My Invoice", text=data)

    syntax_evaluation = report_syntax_v1(invoice)
    syntax_evaluation = Evaluation(**syntax_evaluation)
    
    # "[BR-CL-04]-Invoice currency code MUST be coded using ISO code list 4217 alpha-3" rule
    assert syntax_evaluation.violations[0].rule_id == "BR-CL-03"
    
    # Evaluation is not valid due to fatal error
    assert syntax_evaluation.is_valid == False

def test_syntax_invoice_invalid_not_wellformed():
    # Invalidating the tags so that only one of the tags is capitalised
    data = replace_part_of_string(VALID_INVOICE_TEXT, 2025, 2027, "id")

    invoice = TextInvoice(name="My Invoice", text=data)

    assert report_syntax_v1(invoice)['detail'] == "Invoice is not wellformed"
