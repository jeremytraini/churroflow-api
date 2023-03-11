from typing import Dict
from src.type_structure import *
from src.report import report_get_v1
from src.database import Users, Reports, Violations, Evaluations, db


def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    report = Reports.query.filter_by(id=report_id).one()
    
    return CheckValidReturn(is_valid=report.is_valid, invoice_hash=report.invoice_hash)

def invoice_generate_hash_v1(invoice: Invoice) -> str:
    return "hash"

def invoice_bulk_quick_fix_v1(invoices: List[Invoice]) -> List[Invoice]:
    invoice = Invoice(name="invoice", source="text", data="")
    invoice_list = [invoice]
    return invoice_list
