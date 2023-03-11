import requests
from report import report_generate


def invoice_upload_text_v1(invoice_name: str, invoice_text: str):
    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }


def invoice_upload_url_v1(invoice_name: str, invoice_url: str):
    response = requests.get(data)
    if response.status_code != 200:
        raise Exception("Could not retrieve invoice from url")
    
    invoice_text = response.text

    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }


def invoice_upload_file_v1(invoice_name: str, invoice_file: File()):
    with open(invoice_file, 'rb') as f:
        invoice_text = f.read()
    
    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }

