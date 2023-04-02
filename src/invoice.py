from src.type_structure import *
from src.database import Reports, DoesNotExist
from src.error import InputError, NotFoundError
import requests
from src.generation import generate_report


def invoice_upload_text_v1(invoice_name: str, invoice_text: str, owner = None) -> ReportID:
    if len(invoice_name) > 100:
        raise InputError(detail="Name cannot be longer than 100 characters")
    
    return ReportID(report_id=generate_report(invoice_name, invoice_text, owner))


def invoice_upload_url_v1(invoice_name: str, invoice_url: str, owner = None):
    if len(invoice_name) > 100:
        raise InputError(detail="Name cannot be longer than 100 characters")
    
    try:
        response = requests.get(invoice_url)
    except IOError:
        raise InputError(detail="Could not retrieve invoice from url")
    
    if not (invoice_url.endswith('.txt') or invoice_url.endswith('.xml')):
        raise InputError(detail="URL does not point to plain text or XML data")
    
    invoice_text = response.text
    
    return ReportID(report_id=generate_report(invoice_name, invoice_text, owner))


def invoice_upload_file_v1(invoice_name: str, invoice_text: str, owner = None) -> ReportID:
    if not invoice_name.endswith('.xml'):
        raise InputError(detail="Invoice file type is not XML")
    
    return ReportID(report_id=generate_report(invoice_name, invoice_text, owner))

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    return CheckValidReturn(is_valid=report.is_valid)

def invoice_generate_hash_v1(invoice: TextInvoice) -> str:
    return ""

def invoice_upload_bulk_text_v1(invoices: List[TextInvoice], owner = None) -> ReportIDs:
    return ReportIDs(report_ids=[generate_report(invoice.name, invoice.text, owner) for invoice in invoices])
