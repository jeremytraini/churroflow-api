# from src.types import *
# from tests.server_calls import report_json_report_v1
# from tests.constants import VALID_INVOICE_TEXT
# from tests.helpers import remove_part_of_string, invalidate_invoice

# """
# =====================================
# /report/json_report/v1 TESTS
# =====================================
# """

# # Testing that the report was generated properly and matches input data
# def test_json_valid_invoice():
#     data = VALID_INVOICE_TEXT
    
#     invoice = Invoice(name="My Invoice", source="text", data=data)

#     report = report_json_report_v1(invoice)
#     report = Report(**report)

#     # Report id must be an integer
#     assert isinstance(report.report_id, int)

#     # Date generated must be a string
#     assert isinstance(report.date_generated, str)

#     # Checking for the name of the invoice
#     assert report.invoice_name == "My Invoice"

#     # Checking for raw invoice
#     assert report.invoice_raw == invoice

#     # Invoice hash must be a string
#     assert isinstance(report.invoice_hash, str)

#     # A valid invoice must be a valid report
#     assert report.is_valid

#     # A valid invoice should have 0 violations
#     assert report.total_num_violations == 0
    
#     # Check for wellformedness
#     assert report.wellformedness.aspect == "wellformedness"
#     assert report.wellformedness.is_valid == True
#     assert report.wellformedness.num_rules_failed == 0
#     assert report.wellformedness.num_violations == 0
#     assert report.wellformedness.violations == []

#     # Check for schema
#     assert report.schema_evaluation.aspect == "schema"
#     assert report.schema_evaluation.is_valid == True
#     assert report.schema_evaluation.num_rules_failed == 0
#     assert report.schema_evaluation.num_violations == 0
#     assert report.schema_evaluation.violations == []

#     # Check for syntax
#     assert report.syntax.aspect == "syntax"
#     assert report.syntax.is_valid == True
#     assert report.syntax.num_rules_failed == 0
#     assert report.syntax.num_violations == 0
#     assert report.syntax.violations == []

#     # Check for PEPPOL
#     assert report.peppol.aspect == "peppol"
#     assert report.peppol.is_valid == True
#     assert report.peppol.num_rules_failed == 0
#     assert report.peppol.num_violations == 0
#     assert report.peppol.violations == []

# def test_json_unique_id():
#     data = VALID_INVOICE_TEXT

#     # Creating 2 invoices
#     invoice1 = Invoice(name="Invoice01", source="text", data=data)
#     invoice2 = Invoice(name="Invoice02", source="text", data=data)

#     # Creating 2 reports
#     report1 = report_json_report_v1(invoice1)
#     report1 = Report(**report1)
#     report2 = report_json_report_v1(invoice2)
#     report2 = Report(**report2)

#     # Check that the report_id is not the same
#     report1.report_id != report2.report_id

#     # Check names of the invoice
#     report1.invoice_name == "Invoice01"
#     report2.invoice_name == "Invoice02"

#     # Check that the hash is not the same
#     report1.invoice_hash != report2.invoice_hash

# # Testing that a single rule fails when there is one error in the invoice
# def test_json_single_violation():
#     data = VALID_INVOICE_TEXT
    
#     # Invalidating the currency code
#     data = invalidate_invoice(data, "attrib", "cbc:Amount", "currencyID", "TEST", 1)
    
#     invoice = Invoice(name="Invoice Test", source="text", data=data)

#     report = report_json_report_v1(invoice)
#     report = Report(**report)

#     # Check the name of the invoice
#     assert report.invoice_name == "Invoice Test"

#     # Invalidating a currency code is fatal so report must not be valid
#     assert report.is_valid == False

#     # Only invalidating the currency code - 1 violation
#     assert report.total_num_violations == 1
    
#     # Check for wellformedness
#     assert report.wellformedness.aspect == "wellformedness"
#     assert report.wellformedness.is_valid == True
#     assert report.wellformedness.num_rules_failed == 0
#     assert report.wellformedness.num_violations == 0
#     assert len(report.wellformedness.violations) == 0

#     # Check for schema
#     assert report.schema_evaluation.aspect == "schema"
#     assert report.schema_evaluation.is_valid == True
#     assert report.schema_evaluation.num_rules_failed == 0
#     assert report.schema_evaluation.num_violations == 0
#     assert len(report.schema_evaluation.violations) == 0

#     # Check for syntax
#     assert report.syntax.aspect == "syntax"
#     assert report.syntax.is_valid == False
#     assert report.syntax.num_rules_failed == 1
#     assert report.syntax.num_violations == 1
#     assert len(report.syntax.violations) == 1

#     # Check for PEPPOL
#     assert report.peppol.aspect == "peppol"
#     assert report.peppol.is_valid == True
#     assert report.peppol.num_rules_failed == 0
#     assert report.peppol.num_violations == 0
#     assert len(report.peppol.violations) == 0

# # Testing that multiple violations are generated when there are multiple errors in the invoice
# def test_json_multiple_violations_same_rule():
#     data = VALID_INVOICE_TEXT
    
#     # Invalidating the 2 ABNs
#     data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 1", 1)
#     data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 2", 2)
    
#     invoice = Invoice(name="Invoice Test", source="text", data=data)

#     report = report_json_report_v1(invoice)
#     report = Report(**report)

#     # Invalidating an ABN is only a warning so report must still be valid
#     assert report.is_valid

#     # Invalidating 2 ABNs - 2 violation
#     assert report.total_num_violations == 2
    
#     # Check for wellformedness
#     assert report.wellformedness.aspect == "wellformedness"
#     assert report.wellformedness.is_valid == True
#     assert report.wellformedness.num_rules_failed == 0
#     assert report.wellformedness.num_violations == 0
#     assert len(report.wellformedness.violations) == 0

#     # Check for schema
#     assert report.schema_evaluation.aspect == "schema"
#     assert report.schema_evaluation.is_valid == True
#     assert report.schema_evaluation.num_rules_failed == 0
#     assert report.schema_evaluation.num_violations == 0
#     assert len(report.schema_evaluation.violations) == 0

#     # Check for syntax
#     assert report.syntax.aspect == "syntax"
#     assert report.syntax.is_valid == True
#     assert report.syntax.num_rules_failed == 0
#     assert report.syntax.num_violations == 0
#     assert len(report.syntax.violations) == 0

#     # Check for PEPPOL
#     assert report.peppol.aspect == "peppol"
#     assert report.peppol.is_valid == True
#     assert report.peppol.num_rules_failed == 1
#     assert report.peppol.num_violations == 2
#     assert len(report.peppol.violations) == 2

# def test_json_multiple_violations_different_rules():
#     data = VALID_INVOICE_TEXT
    
#     # Invalidating the 2 ABNs (PEPPOL)
#     data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 1", 1)
#     data = invalidate_invoice(data, "content", "cbc:EndpointID", "", "Not an ABN 2", 2)

#     # Replacing with an tag that is valid but expects a different content type. (Schema)
#     # Also expects the following tag to be different
#     data = invalidate_invoice(data, "tag", "cbc:IssueDate", "", "cbc:CopyIndicator", 1)

#     # Invalidating the 2 Country/IdentificationCode (Syntax)
#     data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'TEST', 1)
#     data = invalidate_invoice(data, 'content', 'cbc:IdentificationCode', '', 'TEST', 2)
    
#     invoice = Invoice(name="Invoice Test", source="text", data=data)

#     report = report_json_report_v1(invoice)
#     report = Report(**report)

#     # Invalidating an ABN is only a warning so report must still be valid
#     assert report.is_valid == False

#     # Violating 6 rules
#     assert report.total_num_violations == 6
    
#     # Check for wellformedness
#     assert report.wellformedness.aspect == "wellformedness"
#     assert report.wellformedness.is_valid == True
#     assert report.wellformedness.num_rules_failed == 0
#     assert report.wellformedness.num_violations == 0
#     assert len(report.wellformedness.violations) == 0

#     # Check for schema
#     assert report.schema_evaluation.aspect == "schema"
#     assert report.schema_evaluation.is_valid == False
#     assert report.schema_evaluation.num_rules_failed == 2
#     assert report.schema_evaluation.num_violations == 2
#     assert len(report.schema_evaluation.violations) == 2

#     # Check for syntax
#     assert report.syntax.aspect == "syntax"
#     assert report.syntax.is_valid == False
#     assert report.syntax.num_rules_failed == 1
#     assert report.syntax.num_violations == 2
#     assert len(report.syntax.violations) == 2

#     # Check for PEPPOL
#     assert report.peppol.aspect == "peppol"
#     assert report.peppol.is_valid == True
#     assert report.peppol.num_rules_failed == 1
#     assert report.peppol.num_violations == 2
#     assert len(report.peppol.violations) == 2

# # Testing invalid wellformedness
# def test_json_invalid_wellformedness():
#     data = VALID_INVOICE_TEXT
    
#     # Removing a closing tag
#     data = remove_part_of_string(data, 11530, 11540)
    
#     invoice = Invoice(name="Invoice Test", source="text", data=data)

#     report = report_json_report_v1(invoice)
#     report = Report(**report)

#     # Removing a closing tag is a fatal error
#     assert report.is_valid == False

#     # Violating 1 rule
#     assert report.total_num_violations == 1
    
#     # Check for wellformedness
#     assert report.wellformedness.aspect == "wellformedness"
#     assert report.wellformedness.is_valid == False
#     assert report.wellformedness.num_rules_failed == 1
#     assert report.wellformedness.num_violations == 1
#     assert len(report.wellformedness.violations) == 1

#     # Invalid wellformedness means no schema, syntax and peppol evaluation
#     assert report.schema_evaluation == None
#     assert report.syntax == None
#     assert report.peppol == None
