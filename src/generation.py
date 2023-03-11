from src.type_structure import *
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from src.helpers import create_temp_file
import requests
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db
from datetime import datetime


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

    # Parse the XSD file
    xsd_doc = etree.parse("src/xsd/maindoc/UBL-Invoice-2.1.xsd")
    xsd = etree.XMLSchema(xsd_doc)
    
    # Parse the XML data
    xml_doc = etree.fromstring(invoice_text.encode("utf-8"))
    
    violations = []
    
    # Validate the XML against the XSD schema
    if not xsd.validate(xml_doc):
        evaluation.is_valid = False
        evaluation.num_errors = 1
        evaluation.num_rules_failed = 1
        
        for error in xsd.error_log:
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


def generate_syntax_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation("syntax", invoice_text)

def generate_peppol_evaluation(invoice_text: str) -> Evaluations:
    return generate_xslt_evaluation("peppol", invoice_text)

def generate_xslt_evaluation(aspect, invoice_text) -> Evaluations:
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        
        if aspect == "syntax":
            xslt_path = "src/validation_artefacts/AUNZ-UBL-validation.xslt"
        else:
            xslt_path = "src/validation_artefacts/AUNZ-PEPPOL-validation.xslt"
        
        executable = xsltproc.compile_stylesheet(stylesheet_file=xslt_path)
        
        if xsltproc.exception_occurred:
            raise Exception("XSLT failed to load! " + xsltproc.error_message)
        
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
    
    report = Reports.create(
        date_generated=datetime.now(),
        invoice_name=invoice_name,
        invoice_raw="Test",
        invoice_hash="Test",
        is_valid=is_valid,
        total_warnings=total_warnings,
        total_errors=total_errors,
        wellformedness=wellformedness_evaluation.id if wellformedness_evaluation else None,
        schema=schema_evaluation.id if schema_evaluation else None,
        syntax=syntax_evaluation.id if syntax_evaluation else None,
        peppol=peppol_evaluation.id if peppol_evaluation else None
    )
    
    print(report)
    print(report.id)
    
    return report.id
