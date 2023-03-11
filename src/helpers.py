from tempfile import NamedTemporaryFile

def create_temp_file(invoice_text: str) -> str:
    tmp = NamedTemporaryFile(mode='w', delete=False)
    tmp.write(invoice_text)
    tmp.close()
    
    return tmp.name
