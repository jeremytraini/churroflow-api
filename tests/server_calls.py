from io import BytesIO
import requests
import json
from src.config import full_url
from src.type_structure import *

# Invoice Endpoints

def invoice_upload_file_v1(invoice_filename: str) -> Server_call_return:
    files = {"file": (invoice_filename, open(invoice_filename, 'rb'))}

    response = requests.post(full_url + 'invoice/upload_file/v1', files=files)

    return json.loads(response.text)

def invoice_bulk_upload_file_v1(invoice_filename1: str, invoice_filename2: str) -> Server_call_return:
    files = {"file1": (invoice_filename1, open(invoice_filename1, 'rb')),
             "file2": (invoice_filename2, open(invoice_filename2, 'rb'))}

    response = requests.post(full_url + 'invoice/bulk_upload_file/v1', files=files)

    return json.loads(response.text)

def invoice_upload_text_v1(invoice_name: str, invoice_text: str) -> Server_call_return:
    payload = TextInvoice(name=invoice_name, text=invoice_text).dict()
    response = requests.post(full_url + 'invoice/upload_text/v1', json=payload)
    
    return json.loads(response.text)

def invoice_upload_text_v2(token: str, invoice_name: str, invoice_text: str) -> Server_call_return:
    payload = TextInvoice(name=invoice_name, text=invoice_text).dict()
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.post(full_url + 'invoice/upload_text/v2', json=payload, headers=headers)
    
    return json.loads(response.text)

def invoice_bulk_upload_text_v1(invoices: List[TextInvoice]) -> Server_call_return:
    payload = {
        "invoices": [invoice.dict() for invoice in invoices]
    }
    response = requests.post(full_url + 'invoice/bulk_upload_text/v1', json=payload)
    
    return json.loads(response.text)

def invoice_upload_url_v1(invoice_name: str, invoice_url: str) -> Server_call_return:
    payload = RemoteInvoice(name=invoice_name, url=invoice_url).dict()
    response = requests.post(full_url + 'invoice/upload_url/v1', json=payload)
    
    return json.loads(response.text)

# Export Endpoints

def export_json_report_v1(report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/json_report/v1', params=payload)

    return json.loads(response.text)

def export_json_report_v2(token: str, report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.get(full_url + 'export/json_report/v2', params=payload, headers=headers)

    return json.loads(response.text)

def export_bulk_json_reports_v1(report_ids) -> Server_call_return:
    payload = report_ids
    response = requests.post(full_url + 'export/bulk_json_reports/v1', json=payload)

    return json.loads(response.text)

def export_bulk_json_reports_v2(token: str, report_ids) -> Server_call_return:
    payload = report_ids
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.post(full_url + 'export/bulk_json_reports/v2', json=payload, headers=headers)

    return json.loads(response.text)

def export_pdf_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/pdf_report/v1', params=payload)
    
    return response.content

def export_pdf_report_v2(token: str, report_id: int):
    payload = {
        "report_id": report_id
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.get(full_url + 'export/pdf_report/v2', params=payload, headers=headers)
    
    return response.content

def export_bulk_pdf_reports_v1(report_ids) -> Server_call_return:
    payload = {
        "report_ids": report_ids
    }
    response = requests.get(full_url + 'export/bulk_pdf_reports/v1', params=payload)

    return json.loads(response.text)

def export_bulk_pdf_reports_v2(token: str, report_ids) -> Server_call_return:
    payload = {
        "report_ids": report_ids
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.get(full_url + 'export/bulk_pdf_reports/v2', params=payload, headers=headers)

    return json.loads(response.text)

def export_html_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/html_report/v1', params=payload)
    
    return response.content

def export_html_report_v2(token: str, report_id: int):
    payload = {
        "report_id": report_id
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.get(full_url + 'export/html_report/v2', params=payload, headers=headers)
    
    return response.content

def export_csv_report_v1(report_id: int):
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'export/csv_report/v1', params=payload)
    
    return response.content

def export_csv_report_v2(token: str, report_id: int):
    payload = {
        "report_id": report_id
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.get(full_url + 'export/csv_report/v2', params=payload, headers=headers)
    
    return response.content

# Report Endpoints

def report_wellformedness_v1(invoice: TextInvoice) -> Server_call_return:
    files = {"file": (invoice.name, BytesIO(invoice.text.encode()))}

    response = requests.post(full_url + 'report/wellformedness/v1', files=files)

    return json.loads(response.text)


def report_schema_v1(invoice: TextInvoice) -> Server_call_return:
    files = {"file": (invoice.name, BytesIO(invoice.text.encode()))}

    response = requests.post(full_url + 'report/schema/v1', files=files)

    return json.loads(response.text)


def report_syntax_v1(invoice: TextInvoice) -> Server_call_return:
    files = {"file": (invoice.name, BytesIO(invoice.text.encode()))}

    response = requests.post(full_url + 'report/syntax/v1', files=files)

    return json.loads(response.text)


def report_peppol_v1(invoice: TextInvoice) -> Server_call_return:
    files = {"file": (invoice.name, BytesIO(invoice.text.encode()))}

    response = requests.post(full_url + 'report/peppol/v1', files=files)

    return json.loads(response.text)

def report_list_all_v1() -> Server_call_return:
    response = requests.get(full_url + 'report/list_all/v1')

    return json.loads(response.text)

def report_list_by_v1(order_by: OrderBy) -> Server_call_return:
    payload = order_by.dict()
    response = requests.get(full_url + 'report/list_by/v1', json=payload)

    return json.loads(response.text)

def report_check_validity_v1(report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    response = requests.get(full_url + 'report/check_validity/v1', params=payload)

    return json.loads(response.text)

### Other Endpoints

def report_delete_v2(token: str, report_id: int) -> Server_call_return:
    payload = {
        "report_id": report_id
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.delete(full_url + 'report/delete/v2', params=payload, headers=headers)
    
    print(response.json())

    return response.json()

def report_change_name_v2(token: str, report_id: int, new_name: str) -> Server_call_return:
    payload = {
        "report_id": report_id,
        "new_name": new_name
    }
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.put(full_url + 'report/change_name/v2', params=payload, headers=headers)

    return json.loads(response.text)

# Linting endpoint

def report_lint_v1(invoice: TextInvoice) -> Server_call_return:
    payload = invoice.dict()
    response = requests.post(full_url + 'report/lint/v1', json=payload)

    return json.loads(response.text)

# Authentication endpoints

def auth_register_v2(name: str, email: str, password: str) -> Server_call_return:
    payload = {
        "name": name,
        "email": email,
        "password": password
    }
    response = requests.post(full_url + 'auth_register/v2', json=payload)

    return json.loads(response.text)


def auth_login_v2(email: str, password: str) -> Server_call_return:
    payload = {
        "username": email,
        "password": password
    }
    response = requests.post(full_url + 'auth_login/v2', data=payload)

    return json.loads(response.text)


def auth_logout_v2():
    response = requests.get(full_url + 'auth_logout/v2')

    return json.loads(response.text)

def health_check_v1():
    response = requests.get(full_url + 'health_check/v1')

    return json.loads(response.text)


def clear_v2(token: str):
    headers = {
        "Authorization": "bearer " + token
    }
    response = requests.delete(full_url + 'clear/v2', headers=headers)
    
    return json.loads(response.text)

