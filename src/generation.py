from src.type_structure import *
from src.constants import XSD_SCHEMA, SYNTAX_EXECUTABLE, PEPPOL_EXECUTABLE
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from src.helpers import create_temp_file
import requests
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db
from datetime import datetime
import hashlib


def generate_wellformedness_evaluation(invoice_text: str) -> Evaluations:
    evaluation = Evaluations(
        is_valid=True,
        num_warnings=0,
        num_errors=0,
        num_rules_failed=0
    )
    
    violations = []

    try:
        etree.fromstring(invoice_text.encode("utf-8"), parser=None)
    except etree.XMLSyntaxError as error:
        evaluation.is_valid = False
        evaluation.num_errors = 1
        evaluation.num_rules_failed = 1
        
        violations.append(Violations(
            rule_id="wellformedness",
            is_fatal=True,
            line=error.lineno,
            column=error.offset,
            message=error.msg
        ))
    
    evaluation.save()
    
    for violation in violations:
        violation.evaluation = evaluation.id 
        violation.save()
    
    return evaluation


def generate_schema_evaluation(invoice_text: str) -> Evaluations:
    evaluation = Evaluations(
        is_valid=True,
        num_warnings=0,
        num_errors=0,
        num_rules_failed=0
    )
    
    # Parse the XML data
    xml_doc = etree.fromstring(invoice_text.encode("utf-8"), parser=None)
    
    violations = []
    
    # Validate the XML against the XSD schema
    if not XSD_SCHEMA.validate(xml_doc):
        evaluation.is_valid = False
        
        for error in XSD_SCHEMA.error_log:
            evaluation.num_errors += 1
            evaluation.num_rules_failed += 1
            
            violations.append(Violations(
                rule_id="wellformedness",
                is_fatal=True,
                line=error.line,
                column=error.column,
                message=error.message
            ))
    
    evaluation.save()
    
    for violation in violations:
        violation.evaluation = evaluation.id 
        violation.save()
    
    return evaluation


def generate_syntax_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation("syntax", invoice_text)

def generate_peppol_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation("peppol", invoice_text)

def generate_xslt_evaluation(aspect, invoice_text) -> Evaluations:
    if (aspect == "syntax"):
        executable = SYNTAX_EXECUTABLE
    else:
        executable = PEPPOL_EXECUTABLE
    
    tmp_filename = create_temp_file(invoice_text)
    schematron_output = executable.transform_to_value(source_file=tmp_filename)
    unlink(tmp_filename)
    
    if not schematron_output:
        raise Exception("Could not generate evaluation due to bad XML!")
    
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
