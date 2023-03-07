from lxml import etree, isoschematron

class Validator:

    def __init__(self, xsd_path: str):
        xmlschema_doc = etree.parse(xsd_path)
        self.xmlschema = etree.XMLSchema(xmlschema_doc)

    def validate(self, xml_path: str) -> bool:
        parser = etree.XMLParser(recover=True)
        xml_doc = etree.parse(xml_path, parser=parser)
        
        self.xmlschema.validate(xml_doc)
            
        for error in self.xmlschema.error_log:
            print("  Line {} Char {}, type {}, level {} : {}".format(error.line, error.column, error.type_name, error.level_name, error.message))
            print()
            
        if self.xmlschema.error_log:
            return False

        return True