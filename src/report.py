import os
from src.classes.Validator_lxml import Validator
from src.types import *

# Syntax report stub
def report_syntax_v1(name, format, source, data) -> Evaluation:
    return {}

# Peppol report stub
def report_peppol_v1(name, format, source, data) -> Evaluation:
    return {}

# Syntax report stub
def report_wellformedness_v1(invoice: Invoice) -> Evaluation:
    return {}

# Peppol report stub
def report_schemavalid_v1(name, format, source, data) -> Evaluation:
    validator = Validator("xsd/maindoc/UBL-Invoice-2.1.xsd")

    # The directory with XML files
    file_path = "AUInvoice.xml"

    if validator.validate(file_path):
        print('Valid! :)')
    else:
        print('Not valid! :(')
    return {}