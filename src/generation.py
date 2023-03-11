from src.type_structure import *
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db

def generate_report(invoice_name: str, invoice_text: str) -> int:
    wellformedness_evaluation_id = generate_wellformedness_evaluation(invoice_text)
    schema_evaluation_id = generate_schema_evaluation(invoice_text)
    syntax_evaluation_id = generate_syntax_evaluation(invoice_text)
    peppol_evaluation_id = generate_peppol_evaluation(invoice_text)
    
    report = Reports.create(
        date_generated="",
        invoice_name="",
        invoice_raw="",
        invoice_hash="",
        is_valid=True,
        total_num_violations=0,
        total_num_warnings=0,
        wellformedness=wellformedness_evaluation_id,
        schema=schema_evaluation_id,
        syntax=syntax_evaluation_id,
        peppol=peppol_evaluation_id
    )
    
    return report.id


def generate_wellformedness_evaluation(invoice_text: str) -> int:
    evaluation = Evaluations(
        aspect="wellformedness",
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
    
    return evaluation.id


def generate_schema_evaluation(invoice_text: str) -> int:
    evaluation = Evaluations(
        aspect="wellformedness",
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
    
    for violation in violations:
        violation.evaluation = evaluation.id 
        violation.save()
    
    return evaluation.id


def generate_syntax_evaluation(invoice_text: str) -> int:
    return generate_xslt_evaluation("syntax", invoice_text)

def generate_peppol_evaluation(invoice_text: str) -> int:
    return generate_xslt_evaluation("peppol", invoice_text)

def create_temp_file(invoice_text: str) -> str:
    tmp = NamedTemporaryFile(mode='w', delete=False)
    tmp.write(invoice_text)
    tmp.close()
    
    return tmp.name

def generate_xslt_evaluation(aspect, invoice_text) -> int:
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        executable = xsltproc.compile_stylesheet(stylesheet_file=xslt_path)
        
        if xsltproc.exception_occurred:
            raise Exception("XSLT failed to load! " + xsltproc.error_message)
        
        tmp_filename = create_temp_file(invoice_text)
        schematron_output = executable.transform_to_value(source_file=tmp_filename)
        unlink(tmp_filename)
        
        if not schematron_output:
            raise Exception("Could not generate evaluation due to bad XML!")
        
        violations = []
        is_valid = True
        rules_failed = set()
        
        output = schematron_output.item_at(0).get_node_value().children[0].children
        
        for item in output:
            if item.name and item.name.endswith("failed-assert"):
                id_name = item.get_attribute_value("id")
                rules_failed.add(id_name)
                is_fatal = item.get_attribute_value("flag") == "fatal"
                
                if is_valid and is_fatal:
                    is_valid = False
                
                xpath = item.get_attribute_value("location")
                test = item.get_attribute_value("test")
                
                message = ""
                if item.children:
                    message = item.children[0].string_value
                
                violations.append({
                    "rule_id": id_name,
                    "is_fatal": is_fatal,
                    "message": message,
                    "suggestion": "suggestion",
                    "test": test,
                    "xpath": xpath
                })
        
        result = Evaluation(
            aspect=aspect,
            is_valid=is_valid,
            num_rules_failed=len(rules_failed),
            num_violations=len(violations),
            violations=violations
        )
        
        return result
