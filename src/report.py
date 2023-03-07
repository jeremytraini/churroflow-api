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
        
        # if not schematron_output:
        #     print(schematron_output.error_message)
        #     print("messed")
        #     exit()
        
        violations = []
        is_valid = True
        rules_failed = set()
        
        output = schematron_output.item_at(0).get_node_value().children[0].children
        
        for item in output:
            if item.name and item.name.endswith("failed-assert"):
                id_name = item.get_attribute_value("id")
                rules_failed.add(id_name)
                flag = item.get_attribute_value("flag")
                
                if is_valid and flag == "fatal":
                    is_valid = False
                    
                # print(item)
                
                location = item.get_attribute_value("location")
                test = item.get_attribute_value("test")
                message = ""
                if item.children:
                    message = item.children[0].string_value
                suggestion = ""
                if len(item.children) > 1:
                    suggestion = item.children[1].string_value
                
                violations.append({
                    "id": id_name,
                    "flag": flag,
                    "location": location,
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
