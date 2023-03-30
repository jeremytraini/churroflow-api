from src.type_structure import *
from src.database import Reports, DoesNotExist
from src.error import InputError
import requests
from src.generation import generate_report


def invoice_upload_text_v1(invoice_name: str, invoice_text: str):
    if len(invoice_name) > 100:
        raise InputError(status_code=400, detail="Name cannot be longer than 100 characters")
    
    return {
        "report_id": generate_report(invoice_name, invoice_text)
    }


def invoice_upload_url_v1(invoice_name: str, invoice_url: str):
    if len(invoice_name) > 100:
        print("here")
        raise InputError(status_code=400, detail="Name cannot be longer than 100 characters")
    
    try:
        response = requests.get(invoice_url)
    except IOError:
        raise InputError(status_code=400, detail="Could not retrieve invoice from url")
    
    if not (invoice_url.endswith('.txt') or invoice_url.endswith('.xml')):
        raise InputError(status_code=400, detail="URL does not point to plain text or XML data")
    
    invoice_text = response.text

    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }


def invoice_upload_file_v1(invoice_name: str, invoice_text: str):
    if not invoice_name.endswith('.xml'):
        raise InputError(status_code=400, detail="Invoice file type is not XML")
    
    return {
        "report_id": generate_report(invoice_name, invoice_text)
    }

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise InputError(status_code=400, detail=f"Report with id {report_id} not found")
    
    return CheckValidReturn(is_valid=report.is_valid)

def invoice_generate_hash_v1(invoice: TextInvoice) -> str:
    return {}

def invoice_upload_bulk_text_v1(invoices: List[TextInvoice]) -> ReportIDs:
    return ReportIDs(report_ids=[generate_report(invoice.name, invoice.text) for invoice in invoices])
