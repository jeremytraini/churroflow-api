from typing import Dict
from saxonche import PySaxonProcessor


# Syntax report stub
def report_syntax_v1(name, format, source, data) -> Dict:
    return {}

# Peppol report stub
def report_peppol_v1(name, format, source, data) -> Dict:
    with PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt30_processor()
        executable = xsltproc.compile_stylesheet(stylesheet_file="AUNZ-PEPPOL-validation.xslt")
        
        node = proc.parse_xml(xml_text=data)
        schematron_output = executable.transform_to_value(source_text=node)
            
        # schematron_output = executable.transform_to_value(source_file="AUInvoice3.xml")
        
        if not schematron_output:
            print(schematron_output.error_message)
            print("messed")
            exit()
        
        violations = []
        is_valid = True
        rules_failed = set()
        
        result = []
        
        return result
