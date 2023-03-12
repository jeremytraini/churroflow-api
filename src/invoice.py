from typing import Dict
from src.type_structure import *
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
    
    report_id = generate_report(invoice_name, invoice_text.decode("utf-8"))
    
    return {
        "report_id": report_id
    }

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    report = Reports.query.filter_by(id=report_id).one() # type: ignore
    
    return CheckValidReturn(is_valid=report.is_valid, invoice_hash=report.invoice_hash)

def invoice_generate_hash_v1(invoice: Invoice) -> str:
    return "hash"

def invoice_bulk_quick_fix_v1(invoices: List[Invoice]) -> List[Invoice]:
    invoice = Invoice(name="invoice", source="text", data="")
    invoice_list = [invoice]
    return invoice_list

def invoice_file_upload_bulk_v1(invoices: List[Invoice]) -> List[int]:
    report_id_list = []
    report_id = 1
    for invoice in invoices:
        report_id_list.append(report_id)
        report_id += 1
     
    return report_id_list