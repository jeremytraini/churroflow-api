from src.type_structure import *
from src.database import Reports, DoesNotExist
import requests
from src.generation import generate_report


def invoice_upload_text_v1(invoice_name: str, invoice_text: str) -> ReportID:
    return ReportID(report_id=generate_report(invoice_name, invoice_text))


def invoice_upload_url_v1(invoice_name: str, invoice_url: str):
    response = requests.get(invoice_url)
    if response.status_code != 200:
        raise Exception("Could not retrieve invoice from url")
    
    invoice_text = response.text
    
    return ReportID(report_id=generate_report(invoice_name, invoice_text))


def invoice_upload_file_v1(invoice_name: str, invoice_text: str) -> ReportID:
    return ReportID(report_id=generate_report(invoice_name, invoice_text))

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    return CheckValidReturn(is_valid=report.is_valid)

def invoice_generate_hash_v1(invoice: TextInvoice) -> str:
    return ""

def invoice_upload_bulk_text_v1(invoices: List[TextInvoice]) -> ReportIDs:
    return ReportIDs(report_ids=[generate_report(invoice.name, invoice.text) for invoice in invoices])
