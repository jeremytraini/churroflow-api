from src.type_structure import *
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db

def generate_report(invoice_name: str, invoice_text: str) -> int:
    pass

def generate_wellformedness_evaluation(invoice_text: str) -> int:
    pass

def generate_schema_evaluation(invoice_text: str) -> int:
    pass

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
