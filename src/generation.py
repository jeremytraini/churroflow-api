from src.type_structure import *
from src.constants import SYNTAX_EXECUTABLE, PEPPOL_EXECUTABLE
from src.database import Reports, Evaluations
from datetime import datetime
import hashlib
from src.validation import get_wellformedness_violations, get_schema_violations, get_xslt_violations
from src.helpers import get_line_from_xpath

def generate_wellformedness_evaluation(invoice_text: str) -> Evaluations:
    violations = get_wellformedness_violations(invoice_text)
    
    return generate_parser_evaluation(violations)

def generate_schema_evaluation(invoice_text: str) -> Evaluations:
    violations = get_schema_violations(invoice_text)
    
    return generate_parser_evaluation(violations)

def generate_parser_evaluation(violations) -> Evaluations:
    evaluation = Evaluations.create(
        is_valid=len(violations) == 0,
        num_warnings=0,
        num_errors=len(violations),
        num_rules_failed=len(violations)
    )
    
    for violation in violations:
        violation.evaluation = evaluation.id #type: ignore
        violation.save()
        
    return evaluation

def generate_syntax_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation(SYNTAX_EXECUTABLE, invoice_text)

def generate_peppol_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation(PEPPOL_EXECUTABLE, invoice_text)

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

def generate_report(invoice_name: str, invoice_text: str, owner) -> int:
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
        invoice_hash=invoice_hash,
        is_valid=is_valid,
        total_warnings=total_warnings,
        total_errors=total_errors,
        wellformedness=wellformedness_evaluation.id if wellformedness_evaluation else None,
        schema=schema_evaluation.id if schema_evaluation else None,
        syntax=syntax_evaluation.id if syntax_evaluation else None,
        peppol=peppol_evaluation.id if peppol_evaluation else None,
        owner=owner
    )
    
    return report.id

def generate_diagnostic_list(invoice_text: str):
    num_errors = 0
    num_warnings = 0
    report = []
    
    wellformedness_violations = get_wellformedness_violations(invoice_text)
    
    for violation in wellformedness_violations:
        if violation.is_fatal:
            num_errors += 1
        else:
            num_warnings += 1
        report.append(LintDiagnostic(
            rule_id=violation.rule_id,
            line=violation.line,
            column=violation.column,
            xpath=violation.xpath,
            message=violation.message,
            suggestion=None,
            severity="error" if violation.is_fatal else "warning"
        ))
    
    if wellformedness_violations:
        return num_errors, num_warnings, report
    
    schema_violations = get_schema_violations(invoice_text)
    
    for violation in schema_violations:
        if violation.is_fatal:
            num_errors += 1
        else:
            num_warnings += 1
        report.append(LintDiagnostic(
            rule_id=violation.rule_id,
            line=violation.line,
            column=violation.column,
            xpath=violation.xpath,
            message=violation.message,
            suggestion=None,
            severity="error" if violation.is_fatal else "warning"
        ))
    
    if schema_violations:
        return num_errors, num_warnings, report

    syntax_violations, _, _, _ = get_xslt_violations(SYNTAX_EXECUTABLE, invoice_text)
    peppol_violations, _, _, _ = get_xslt_violations(PEPPOL_EXECUTABLE, invoice_text)
    
    for violation in syntax_violations + peppol_violations:
        if violation.is_fatal:
            num_errors += 1
        else:
            num_warnings += 1
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
    
    return num_errors, num_warnings, report