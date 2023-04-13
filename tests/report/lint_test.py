from src.type_structure import *
from tests.server_calls import report_lint_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice

"""
=====================================
/report/lint/v1 TESTS
=====================================
"""

# Testing that the report was generated properly and matches input data
def test_lint_valid_invoice():
    data = VALID_INVOICE_TEXT
    
    invoice = TextInvoice(name="My Invoice", text=data)

    lint_report = report_lint_v1(invoice)
    
    assert lint_report == {
        "num_errors": 0,
        "num_warnings": 0,
        "report": []
    }


def test_lint_warning_in_invoice():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the ABN, changing the content of the ABN
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN', 1)
    
    invoice = TextInvoice(name="My Invoice", text=data)

    lint_report = report_lint_v1(invoice)['report']
    
    assert len(lint_report) == 1
    
    # Checking correct rule id was triggered
    assert lint_report[0]['rule_id'] == 'PEPPOL-COMMON-R050'
    
    # This error is on line 39, and no column is specified
    assert lint_report[0]['line'] == 40
    assert lint_report[0]['column'] == 0
    
    # Checking there is a message, suggestion, xpath
    assert lint_report[0]['message']
    assert lint_report[0]['suggestion']
    assert lint_report[0]['xpath']
    
    # Checking severity value is correct
    assert lint_report[0]['severity'] == 'warning'
    
def test_lint_tag_order_invalid():
    # Invalidating the date
    data = invalidate_invoice(VALID_INVOICE_TEXT, "tag", "cbc:IssueDate", "", "cbc:DueDate", 1)
    data = invalidate_invoice(data, "tag", "cbc:DueDate", "", "cbc:IssueDate", 2)
    invoice = TextInvoice(name="My Invoice", text=data)

    lint_report = report_lint_v1(invoice)['report']
    
    assert len(lint_report) == 1
    assert lint_report[0] == {'rule_id': 'schema',
                              'line': 5,
                              'column': 0,
                              'message': lint_report[0]['message'],
                              'suggestion': None,
                              'xpath': None,
                              'severity': 'error'}

def test_lint_many_syntax_and_peppol():
    data = VALID_INVOICE_TEXT
    
    # Invalidating the 2 ABNs
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 1', 1)
    data = invalidate_invoice(data, 'content', 'cbc:EndpointID', '', 'Not an ABN 2', 2)
    
    # Adding 1 'cbc:ProfileExecutionID' tag
    # data = invalidate_invoice(data, 'tag', 'cbc:Note', '', 'cbc:ProfileExecutionID', 1)
    data = invalidate_invoice(data, 'attrib', 'cbc:Amount', 'currencyID', 'TEST', 1)
    
    invoice = TextInvoice(name="My Invoice", text=data)
    
    lint_report = report_lint_v1(invoice)['report']
    
    assert sum(violation['rule_id'] == 'PEPPOL-COMMON-R050' for violation in lint_report) == 2
    assert sum(violation['rule_id'] == 'BR-CL-03' for violation in lint_report) == 1
