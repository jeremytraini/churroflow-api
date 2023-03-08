from typing import Dict

from src.types import *

def invoice_quick_fix_wellformedness_v1(report_id) -> Dict:
    return {}

def invoice_quick_fix_syntax_v1(report_id) -> Dict:
    return {}

def invoice_quick_fix_peppol_v1(report_id) -> Dict:
    return {}

def invoice_quick_fix_schema_v1(report_id) -> Dict:
    return {}

def invoice_check_validity_v1(report_id) -> Dict:
    return {}

def invoice_generate_hash_v1(invoice) -> Dict:
    return {}

def invoice_bulk_quick_fix_v1(invoices) -> list[Invoice]:
    invoice = Invoice(name="invoice", format="XML", source="text", data="")
    invoice_list = [invoice]
    return invoice_list
