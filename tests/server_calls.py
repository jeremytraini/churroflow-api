import requests
import json
from src.config import full_url
from src.type_structure import *


# Invoice Endpoints

def invoice_upload_text_v1(invoice_name: str, invoice_text: str) -> Server_call_return:
    payload = {
        "invoice_name": invoice_name,
        "invoice_text": invoice_text
    }
    response = requests.post(full_url + 'invoice/upload_text/v1', params=payload)
    
    return json.loads(response.text)

def invoice_upload_url_v1(invoice_name: str, invoice_url: str) -> Server_call_return:
    payload = {
        "invoice_name": invoice_name,
        "invoice_url": invoice_url
    }
    response = requests.post(full_url + 'invoice/upload_url/v1', params=payload)
    
    return json.loads(response.text)

def invoice_upload_file_v1(invoice_name: str, invoice_filename) -> Server_call_return:
    headers = {
        "invoice_name": invoice_name
    }

    files = {"file": (invoice_filename, open(invoice_filename, 'rb'))}

    response = requests.post(full_url + 'invoice/upload_file/v1', files=files, headers=headers)
    
    return json.loads(response.text)


# Export Endpoints

def export_json_report_v1(report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    response = requests.post(full_url + 'export/json_report/v1', params=payload)
    
    return json.loads(response.text)

def export_pdf_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.post(full_url + 'export/pdf_report/v1', params=payload)
    
    with open(path, 'wb') as s:
        s.write(data)
    
    return response.content

def export_html_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.post(full_url + 'export/html_report/v1', params=payload)
    
    return response.content

def export_csv_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.post(full_url + 'export/csv_report/v1', params=payload)
    
    return response.content

# Report Endpoints

def report_wellformedness_v1(invoice: Invoice) -> Server_call_return:
    payload = invoice.dict()
    response = requests.post(full_url + 'report/wellformedness/v1', json=payload)
    
    return json.loads(response.text)


def report_schema_v1(invoice: Invoice) -> Server_call_return:
    payload = invoice.dict()
    response = requests.post(full_url + 'report/schema/v1', json=payload)

    return json.loads(response.text)


def report_syntax_v1(invoice: Invoice) -> Server_call_return:
    payload = invoice.dict()
    response = requests.post(full_url + 'report/syntax/v1', json=payload)

    return json.loads(response.text)


def report_peppol_v1(invoice: Invoice) -> Server_call_return:
    payload = invoice.dict()
    response = requests.post(full_url + 'report/peppol/v1', json=payload)

    return json.loads(response.text)


# Other Endpoints

def health_check_v1():
    response = requests.get(full_url + 'health_check/v1')

    return json.loads(response.text)


def clear_v1():
    payload = {
        
    }
    response = requests.delete(full_url + 'clear/v1', json=payload)
    
    return json.loads(response.text)

