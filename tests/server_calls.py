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

def invoice_file_upload_bulk_v1(invoices: List[Invoice]) -> Server_call_return:
    payload = [invoice.dict() for invoice in invoices]
    response = requests.post(full_url + 'invoice/file_upload_bulk/v1', json=payload)
    
    return json.loads(response.text)

# Export Endpoints

def export_json_report_v1(report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/json_report/v1', params=payload)
    
    return json.loads(response.text)

def export_pdf_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/pdf_report/v1', params=payload)
    
    return response.content

def export_html_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/html_report/v1', params=payload)
    
    return response.content

def export_csv_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/csv_report/v1', params=payload)
    
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

def report_list_all_v1() -> Server_call_return:
    response = requests.get(full_url + 'report/list_all/v1')

    return json.loads(response.text)

def report_list_by_v1(order_by: OrderBy) -> Server_call_return:
    payload = order_by.dict()
    response = requests.get(full_url + 'report/list_by/v1', json=payload)

    return json.loads(response.text)

def report_delete_v1(report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    response = requests.delete(full_url + 'report/delete/v1', params=payload)

    return json.loads(response.text)

def report_change_name_v1(report_id: int, new_name: str) -> Server_call_return:
    payload = {
        "report_id": report_id,
        "new_name": new_name
    }
    response = requests.put(full_url + 'report/change_name/v1', params=payload)

    return json.loads(response.text)

def report_check_validity_v1(report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'report/check_validity/v1', params=payload)

    return json.loads(response.text)


def report_bulk_export_v1(report_ids: List[int], report_format: Format) -> Server_call_return:
    payload = {
        "report_ids": report_ids,
        "report_format": report_format.format
    }
    response = requests.get(full_url + 'report/bulk_export/v1', json=payload)

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

