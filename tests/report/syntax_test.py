# from tests.server_calls import report_syntax_v1
# from tests.constants import VALID_INVOICE_TEXT
# from tests.helpers import remove_part_of_string

# """
# =====================================
# /report/syntax/v1 TESTS
# =====================================
# """

# # Testing that the report was generated properly and matches input data
# def test_syntax_valid_invoice():
#     name = "My Invoice"
#     format = "xml"
#     source = "text"
#     data = VALID_INVOICE_TEXT
    
#     syntax_evaluation = report_syntax_v1(name, format, source, data)
#     assert syntax_evaluation["aspect"] == "syntax"
    
#     # We expect many rules to be fired for any invoice
#     # This depends on the number of rules in the rule set but should be at least 1
#     assert syntax_evaluation["num_rules_fired"] > 0
    
#     # We expect no rules to fail for a valid invoice
#     assert syntax_evaluation["num_rules_failed"] == 0
    
#     # We expect no violations for a valid invoice
#     assert syntax_evaluation["num_violations"] == 0
    
#     # The violation list should be empty for a valid invoice
#     assert len(syntax_evaluation["violations"]) == 0

# # Testing that a single rule fails when there is one error in the invoice
# def test_syntax_single_volation():
#     name = "My Invoice"
#     format = "xml"
#     source = "text"
#     data = VALID_INVOICE_TEXT
    
#     # Invalidating the currency code
#     data = data[:864] + "D" + data[865:]
    
#     syntax_evaluation = report_syntax_v1(name, format, source, data)
    
#     # We expect exactly 1 rule to fail due to the invalid currency code
#     assert syntax_evaluation["num_rules_failed"] == 1
    
#     # We expect exactly 1 violation due to the invalid currency code
#     assert syntax_evaluation["num_violations"] == 1
    
#     # Thus there should be exactly 1 violation in the violation list
#     assert len(syntax_evaluation["violations"]) == 1
    
#     code_violation = syntax_evaluation["violations"][0]
    
#     # From 'A-NZ_Invoice_Extension_v1.0.8.docx' file:
#     # BR-CL-04 | [BR-CL-04]-Invoice currency code MUST be coded using ISO code list 4217 alpha-3 | Same | fatal
    
#     # Check that the violation is for the correct rule and is flagged as fatal
#     assert code_violation["rule_id"] == "BR-CL-04"
#     assert code_violation["is_fatal"] == True
    
#     # Check that the violation has a non-empty message, test and suggestion
#     assert code_violation["message"]
#     assert code_violation["test"]
#     assert code_violation["suggestion"]
    
#     assert code_violation["location"]["type"] == "xpath"
    
#     # Check that the location xpath is not empty
#     assert code_violation["location"]["xpath"]


# # Testing that multiple violations are generated when there are multiple errors in the invoice
# def test_syntax_multiple_violations_same_rule():
#     name = "My Invoice"
#     format = "xml"
#     source = "text"
#     data = VALID_INVOICE_TEXT
    
#     # Invalidating the 2 currency codes
#     data = data[:864] + "D" + data[865:]
#     data = data[:1288] + "D" + data[1289:]
    
#     syntax_evaluation = report_syntax_v1(name, format, source, data)
    
#     # We expect exactly 1 distinct rule to fail
#     assert syntax_evaluation["num_rules_failed"] == 1
    
#     # We expect exactly 2 violations for each invalid currency code
#     assert syntax_evaluation["num_violations"] == 2
    
#     # Thus there should be exactly 2 violations in the violation list
#     assert len(syntax_evaluation["violations"]) == 2
    
#     code_violation1 = syntax_evaluation["violations"][0]
#     code_violation2 = syntax_evaluation["violations"][1]
    
#     # Rule IDs should be the same
#     assert code_violation1["rule_id"] == code_violation2["rule_id"] == "BR-CL-04"
    
#     # Locations should be different for each violation
#     assert code_violation1["location"] != code_violation2["location"]


# def test_syntax_multiple_violations_different_rules():
#     name = "My Invoice"
#     format = "xml"
#     source = "text"
#     data = VALID_INVOICE_TEXT
    
#     # Invalidating 2 currency codes
#     data = data[:864] + "D" + data[865:]
#     data = data[:1288] + "D" + data[1289:]
    
#     # Invalidating the 2 addresses
#     data = remove_part_of_string(data, 2061, 2062)
#     data = remove_part_of_string(data, 3508, 3509)
    
#     syntax_evaluation = report_syntax_v1(name, format, source, data)
    
#     # We expect exactly 2 distinct rules to fail
#     assert syntax_evaluation["num_rules_failed"] == 2
    
#     # We expect exactly 2 violations for each invalid currency code and 2 violations for each invalid address
#     assert syntax_evaluation["num_violations"] == 4
    
#     # Thus there should be exactly 4 violations in the violation list
#     assert len(syntax_evaluation["violations"]) == 4
    
#     code_violation1 = syntax_evaluation["violations"][0]
#     code_violation2 = syntax_evaluation["violations"][1]
#     address_violation1 = syntax_evaluation["violations"][2]
#     address_violation2 = syntax_evaluation["violations"][3]
    
#     # Rule IDs should be the same for each currency code violation
#     assert code_violation1["rule_id"] == code_violation2["rule_id"] == "BR-CL-04"
    
#     # Rule IDs should be the same for each address violation
#     assert address_violation1["rule_id"] == address_violation2["rule_id"] == "BR-CL-05"
    
#     # Locations should be different for each violation
#     assert code_violation1["location"] != code_violation2["location"]
#     assert address_violation1["location"] != address_violation2["location"]


# # Testing that a warning doesn't invalidate the report
# def test_syntax_warning_doesnt_invalidate_report():
#     name = "My Invoice"
#     format = "xml"
#     source = "text"
#     data = VALID_INVOICE_TEXT
    
#     # Adding "D" to the currency code to make it invalid
#     data = data[:864] + "D" + data[865:]
    
#     syntax_evaluation = report_syntax_v1(name, format, source, data)
    
#     # Currency code warning rule
#     assert syntax_evaluation["violations"][0]["rule_id"] == "BR-CL-04"
    
#     # Evaluation still valid
#     assert syntax_evaluation["is_valid"] == True

    
# # Testing that a fatal error does invalidate the report
# def test_syntax_fatal_error_invalidates_report():
#     name = "My Invoice"
#     format = "xml"
#     source = "text"
#     data = VALID_INVOICE_TEXT
    
#     # Adding "D" to the currency code to make it invalid
#     data = data[:864] + "D" + data[865:]
    
#     syntax_evaluation = report_syntax_v1(name, format, source, data)
    
#     # "[BR-CL-04]-Invoice currency code MUST be coded using ISO code list 4217 alpha-3" rule
#     assert syntax_evaluation["violations"][0]["rule_id"] == "BR-CL-04"
    
#     # Evaluation is not valid due to fatal error
#     assert syntax_evaluation["is_valid"] == False


