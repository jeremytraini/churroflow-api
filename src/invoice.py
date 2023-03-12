from typing import Dict
from src.type_structure import *
from src.report import report_get_v1
from src.database import Users, Reports, Violations, Evaluations, db
import requests
from src.generation import generate_report


def invoice_upload_text_v1(invoice_name: str, invoice_text: str):
    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }


def invoice_upload_url_v1(invoice_name: str, invoice_url: str):
    response = requests.get(invoice_url)
    if response.status_code != 200:
        raise Exception("Could not retrieve invoice from url")
    
    invoice_text = response.text

    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }


def invoice_upload_file_v1(invoice_name: str, invoice_file):
    with open(invoice_file, 'rb') as f:
        invoice_text = f.read()
    
    report_id = generate_report(invoice_name, invoice_text)
    
    return {
        "report_id": report_id
    }

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    return CheckValidReturn(is_valid=report.is_valid)

def invoice_generate_hash_v1(invoice: Invoice) -> str:
    return "hash"

def invoice_bulk_quick_fix_v1(invoices: List[Invoice]) -> List[Invoice]:
    invoice = Invoice(name="invoice", source="text", data="")
    invoice_list = [invoice]
    return invoice_list
