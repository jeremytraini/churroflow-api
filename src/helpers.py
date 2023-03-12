from tempfile import NamedTemporaryFile
from src.type_structure import *

def create_temp_file(invoice_text: str) -> str:
    tmp = NamedTemporaryFile(mode='w', delete=False)
    tmp.write(invoice_text)
    tmp.close()
    
    return tmp.name

def extract_text_from_invoice(invoice: Invoice) -> str:
    if invoice.source == "url":
        response = requests.get(invoice.data)
        if response.status_code != 200:
            raise Exception("Could not retrieve file from url")

        data = response.text
    elif invoice.source == "text":
        data = invoice.data
    else:
        raise Exception("Invalid source, please enter url or text")

    return data
