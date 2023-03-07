from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests


def generate_xslt_evaluation(invoice_text, xslt_path) -> Dict:
    with PySaxonProcessor(license=False) as proc:
        
        print(xslt_path)
        
        xsltproc = proc.new_xslt30_processor()
        executable = xsltproc.compile_stylesheet(stylesheet_file=xslt_path)
        
        if xsltproc.exception_occurred:
            raise Exception("XSLT failed to load! " + xsltproc.error_message)
        
        if executable.exception_occurred:
            raise Exception("Executable failed to load! " + executable.error_message)
        
        print(len(invoice_text))
        
        tmp = NamedTemporaryFile(mode='w', delete=False)
        tmp.write(invoice_text)
        tmp.close()
        
        schematron_output = executable.transform_to_value(source_file=tmp.name)
        
        if not schematron_output:
            raise Exception("Schematron output is empty")
        
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
                
                location = item.get_attribute_value("location")
                test = item.get_attribute_value("test")
                message = ""
                if item.children:
                    message = item.children[0].string_value
                suggestion = ""
                if len(item.children) > 1:
                    suggestion = item.children[1].string_value
                
                violations.append({
                    "rule_id": id_name,
                    "is_fatal": is_fatal,
                    "location": {
                                    "type": "xpath",
                                    "xpath": location
                                    },
                    "test": test,
                    "message": message,
                    "suggestion": suggestion
                })
        
        result =  {
            "aspect": "peppol",
            "is_valid": is_valid,
            "num_rules_fired": len(output),
            "num_rules_failed": len(rules_failed),
            "num_violations": len(violations),
            "violations": violations
        }
        
        return result


# Syntax report stub
def report_syntax_v1(name, format, source, data) -> Dict:
    return {}


def report_peppol_v1(name, format, source, data) -> Dict:
    if source == "file":
        with open(data, 'r') as f:
            data = f.read()
    elif source == "url":
        response = requests.get(data)
        if response.status_code != 200:
            raise Exception("Could not retrieve file from url")

        data = response.text
    
    return generate_xslt_evaluation(data, "src/validation_artefacts/AUNZ-PEPPOL-validation.xslt")
        
    
