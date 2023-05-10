from src.type_structure import *
from src.constants import XSD_SCHEMA
from lxml import etree
from src.helpers import create_temp_file
from os import unlink
from src.database import Violations
from src.error import InputError


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

def get_xslt_violations(executable, invoice_text: str):
    tmp_filename = create_temp_file(invoice_text)
    schematron_output = executable.transform_to_value(source_file=tmp_filename)
    unlink(tmp_filename)
    
    if not schematron_output:
        raise InputError("Could not generate evaluation due to invalid XML!")
    
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
