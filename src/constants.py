from lxml import etree
from saxonche import PySaxonProcessor

# Parse the XSD file
XSD_SCHEMA = etree.XMLSchema(etree.parse("src/xsd/maindoc/UBL-Invoice-2.1.xsd", parser=None))
proc = PySaxonProcessor(license=False)
xsltproc = proc.new_xslt30_processor()
SYNTAX_EXECUTABLE = xsltproc.compile_stylesheet(stylesheet_file="src/validation_artefacts/AUNZ-UBL-validation.xslt")
PEPPOL_EXECUTABLE = xsltproc.compile_stylesheet(stylesheet_file="src/validation_artefacts/AUNZ-PEPPOL-validation.xslt")

# The token below is a temporary token for Sprint 1.
# It will be replaced with a token that is generated by Auth endpoints.
ADMIN_TOKEN = "UG#&*GFUBIFBIUEB#&*FUB"

