from src.type_structure import *
from src.constants import XSD_SCHEMA, SYNTAX_EXECUTABLE, PEPPOL_EXECUTABLE
from lxml import etree
from src.helpers import create_temp_file
from os import unlink
from src.database import Reports, Violations, Evaluations, db
from datetime import datetime
import hashlib
import re

def get_wellformedness_violations(invoice_text: str) -> List[Violation]:
    violations = []
    
    try:
        etree.fromstring(invoice_text.encode("utf-8"), parser=None)
    except etree.XMLSyntaxError as error:
        violations.append(Violations(
            rule_id="wellformedness",
            is_fatal=True,
            line=error.lineno,
            column=error.offset,
            message=error.msg
        ))
    
    return violations

def generate_wellformedness_evaluation(invoice_text: str) -> Evaluations:
    violations = get_wellformedness_violations(invoice_text)
    
    evaluation = Evaluations.create(
        is_valid=True if len(violations) == 0 else False,
        num_warnings=0,
        num_errors=len(violations),
        num_rules_failed=len(violations)
    )
    
    for violation in violations:
        violation.evaluation = evaluation.id 
        violation.save()
    
    return evaluation

def get_schema_violations(invoice_text: str):
    # Parse the XML data
    xml_doc = etree.fromstring(invoice_text.encode("utf-8"), parser=None)
    nsmap = {"{"+v+"}": k+":" if k is not None else "" for k, v in xml_doc.nsmap.items()}
    
    violations = []
    
    # Validate the XML against the XSD schema
    if not XSD_SCHEMA.validate(xml_doc):
        for error in XSD_SCHEMA.error_log:
            message = error.message
            for k, v in nsmap.items():
                message = message.replace(k, v)
            violations.append(Violations(
                rule_id="schema",
                is_fatal=True,
                line=error.line,
                column=error.column,
                message=message
            ))
    
    return violations

def generate_schema_evaluation(invoice_text: str) -> Evaluations:
    violations = get_schema_violations(invoice_text)
    
    evaluation = Evaluations.create(
        is_valid=True if len(violations) == 0 else False,
        num_warnings=0,
        num_errors=len(violations),
        num_rules_failed=len(violations)
    )
    
    for violation in violations:
        violation.evaluation = evaluation.id 
        violation.save()
    
    return evaluation

def generate_syntax_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation(SYNTAX_EXECUTABLE, invoice_text)

def generate_peppol_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation(PEPPOL_EXECUTABLE, invoice_text)

def get_xslt_violations(executable, invoice_text: str):
    tmp_filename = create_temp_file(invoice_text)
    schematron_output = executable.transform_to_value(source_file=tmp_filename)
    unlink(tmp_filename)
    
    if not schematron_output:
        raise Exception("Could not generate evaluation due to invalid XML!")
    
    violations = []
    
    num_warnings = 0
    num_errors = 0
    rules_failed = set()
    
    output = schematron_output.item_at(0).get_node_value().children[0].children
    
    for item in output:
        if item.name and item.name.endswith("failed-assert"):
            id_name = item.get_attribute_value("id")
            rules_failed.add(id_name)
            is_fatal = item.get_attribute_value("flag") == "fatal"
            
            if is_fatal:
                num_errors += 1
            else:
                num_warnings += 1
            
            xpath = item.get_attribute_value("location")
            test = item.get_attribute_value("test")
            
            message = ""
            suggestion = ""
            if item.children:
                message = item.children[0].string_value
                
                if len(item.children) > 1:
                    suggestion = item.children[1].string_value
            
            violations.append(Violations(
                rule_id=id_name,
                is_fatal=is_fatal,
                xpath=xpath,
                test=test,
                message=message,
                suggestion=suggestion
            ))
    
    return violations, num_warnings, num_errors, rules_failed

def generate_xslt_evaluation(executable, invoice_text) -> Evaluations:
    violations, num_warnings, num_errors, rules_failed = get_xslt_violations(executable, invoice_text)
    
    evaluation = Evaluations.create(
        is_valid=num_errors == 0,
        num_warnings=num_warnings,
        num_errors=num_errors,
        num_rules_failed=len(rules_failed)
    )
    
    for violation in violations:
        violation.evaluation = evaluation.id 
        violation.save()
    
    return evaluation

def generate_report(invoice_name: str, invoice_text: str) -> int:
    wellformedness_evaluation = None
    schema_evaluation = None
    syntax_evaluation = None
    peppol_evaluation = None
    
    wellformedness_evaluation = generate_wellformedness_evaluation(invoice_text)
    total_errors = wellformedness_evaluation.num_errors
    is_valid = wellformedness_evaluation.is_valid
    total_warnings = 0
    
    if wellformedness_evaluation.is_valid:
        schema_evaluation = generate_schema_evaluation(invoice_text)
        total_errors = schema_evaluation.num_errors
        is_valid = schema_evaluation.is_valid
        
        if schema_evaluation.is_valid:
            syntax_evaluation = generate_syntax_evaluation(invoice_text)
            peppol_evaluation = generate_peppol_evaluation(invoice_text)
            
            total_warnings = syntax_evaluation.num_warnings + peppol_evaluation.num_warnings
            total_errors = syntax_evaluation.num_errors + peppol_evaluation.num_errors
            
            is_valid = peppol_evaluation.is_valid and syntax_evaluation.is_valid
    
    invoice_hash = int(hashlib.sha1(invoice_text.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
    
    report = Reports.create(
        date_generated=datetime.now(),
        invoice_name=invoice_name,
        invoice_text=invoice_text,
        invoice_hash=invoice_hash,
        is_valid=is_valid,
        total_warnings=total_warnings,
        total_errors=total_errors,
        wellformedness=wellformedness_evaluation.id if wellformedness_evaluation else None,
        schema=schema_evaluation.id if schema_evaluation else None,
        syntax=syntax_evaluation.id if syntax_evaluation else None,
        peppol=peppol_evaluation.id if peppol_evaluation else None
    )
    
    return report.id

def fix_xpath(string):
    def repl(match):
        element_name = match.group(1)
        return f'/*[local-name()=\'{element_name}\']['
    
    pattern = r'\/\*:([A-Za-z]+)\['
    return re.sub(pattern, repl, string)

def get_element_from_xpath(xml_text: str, xpath_expression: str) -> etree.Element:
    root = etree.fromstring(xml_text.encode('utf-8'))

    # Evaluate the XPath expression to get the matching element
    try:
        return root.xpath(fix_xpath(xpath_expression))[0]
    except etree.XPathEvalError:
        return None

def get_line_from_xpath(xml_text: str, xpath_expression: str) -> int:
    element = get_element_from_xpath(xml_text, xpath_expression)
    if element is None:
        return 0
        
    return element.sourceline

def generate_diagnostic_list(invoice_text: str) -> int:
    report = []
    
    wellformedness_violations = get_wellformedness_violations(invoice_text)
    
    for violation in wellformedness_violations:
        report.append(LintDiagnostic(
            rule_id=violation.rule_id,
            line=violation.line,
            column=violation.column,
            xpath=violation.xpath,
            message=violation.message,
            severity="error" if violation.is_fatal else "warning"
        ))
    
    if wellformedness_violations:
        return report
    
    schema_violations = get_schema_violations(invoice_text)
    
    for violation in schema_violations:
        report.append(LintDiagnostic(
            rule_id=violation.rule_id,
            line=violation.line,
            column=violation.column,
            xpath=violation.xpath,
            message=violation.message,
            severity="error" if violation.is_fatal else "warning"
        ))
    
    if schema_violations:
        return report

    syntax_violations, _, _, _ = get_xslt_violations(SYNTAX_EXECUTABLE, invoice_text)
    peppol_violations, _, _, _ = get_xslt_violations(PEPPOL_EXECUTABLE, invoice_text)
    
    for violation in syntax_violations + peppol_violations:
        line = get_line_from_xpath(invoice_text, violation.xpath)
        report.append(LintDiagnostic(
            rule_id=violation.rule_id,
            line=line,
            column=0,
            xpath=violation.xpath,
            message=violation.message,
            suggestion=violation.suggestion,
            severity="error" if violation.is_fatal else "warning"
        ))
    
    return report