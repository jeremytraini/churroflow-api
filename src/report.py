from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests

def invoice_preprocessor(name, format, source, data):
    if source == "file":
        with open(data, 'r') as f:
            return f.read()
    elif source == "url":
        response = requests.get(data)
        if response.status_code != 200:
            raise Exception("Could not retrieve invoice from url")

        return response.text
    elif source == "text":
        return data

def report_json_report_v1(name, format, source, data) -> Dict:
    return {}

def report_visual_report_v1(name, format, source, data, report_format) -> Dict:
    return {}

def report_wellformedness_v1(name, format, source, data) -> Dict:
    return {}

def report_schema_v1(name, format, source, data) -> Dict:
    return {}

def report_syntax_v1(name, format, source, data) -> Dict:
    invoice_text = invoice_preprocessor(name, format, source, data)
    
    return generate_xslt_evaluation("syntax", invoice_text, "src/validation_artefacts/AUNZ-UBL-validation.xslt")

def report_peppol_v1(name, format, source, data) -> Dict:
    invoice_text = invoice_preprocessor(name, format, source, data)
    
    return generate_xslt_evaluation("peppol", invoice_text, "src/validation_artefacts/AUNZ-PEPPOL-validation.xslt")

def report_get_v1(report_id) -> Dict:
    return {}

def report_list_all_v1(order_by) -> Dict:
    return {}

def report_list_score_v1(score, order_by) -> Dict:
    return {}

def report_export_v1(report_id, report_format) -> Dict:
    return {}

def report_change_name_v1(report_id, new_name) -> Dict:
    return {}

def report_delete_v1(report_id) -> Dict:
    return {}

def report_bulk_generate_v1(invoices) -> Dict:
    return {}

def report_bulk_export_v1(report_ids, report_format) -> Dict:
    return {}

def report_bulk_export_v1(report_ids, report_format) -> Dict:
    return {}

# Helper functions

def generate_xslt_evaluation(aspect, invoice_text, xslt_path) -> Dict:
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
            "aspect": aspect,
            "is_valid": is_valid,
            "num_rules_fired": len(output),
            "num_rules_failed": len(rules_failed),
            "num_violations": len(violations),
            "violations": violations
        }
        
        return result
