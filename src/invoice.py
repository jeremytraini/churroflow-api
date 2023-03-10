from typing import Dict

from src.types import *
from src.report import report_get_v1

def invoice_quick_fix_wellformedness_v1(report_id: int) -> Quick_Fix_Return:
    invoice = Invoice(name="My Invoice", source="text", data="data")
    report = Report(
        report_id=0,
        score=0,
        date_generated="",
        invoice_name="",
        invoice_raw="",
        invoice_hash="",
        is_valid=True,
        total_num_violations=0,
        wellformedness=None,
        schema_evaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = Quick_Fix_Return (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_quick_fix_syntax_v1(report_id: int) -> Quick_Fix_Return:
    invoice = Invoice(name="My Invoice", source="text", data="data")
    report = Report(
        report_id=0,
        score=0,
        date_generated="",
        invoice_name="",
        invoice_raw="",
        invoice_hash="",
        is_valid=True,
        total_num_violations=0,
        wellformedness=None,
        schema_evaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = Quick_Fix_Return (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_quick_fix_peppol_v1(report_id: int) -> Quick_Fix_Return:
    invoice = Invoice(name="My Invoice", source="text", data="data")
    report = Report(
        report_id=0,
        score=0,
        date_generated="",
        invoice_name="",
        invoice_raw="",
        invoice_hash="",
        is_valid=True,
        total_num_violations=0,
        wellformedness=None,
        schema_evaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = Quick_Fix_Return (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_quick_fix_schema_v1(report_id: int) -> Quick_Fix_Return:
    invoice = Invoice(name="My Invoice", source="text", data="data")
    report = Report(
        report_id=0,
        score=0,
        date_generated="",
        invoice_name="",
        invoice_raw="",
        invoice_hash="",
        is_valid=True,
        total_num_violations=0,
        wellformedness=None,
        schema_evaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = Quick_Fix_Return (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_check_validity_v1(report_id: int) -> Check_Valid_Return:
    report = report_get_v1(report_id)
    return Check_Valid_Return(is_valid=report.is_valid, invoice_hash=report.invoice_hash)

def invoice_generate_hash_v1(invoice: Invoice) -> str:
    return "hash"

def invoice_bulk_quick_fix_v1(invoices: List[Invoice]) -> List[Invoice]:
    invoice = Invoice(name="invoice", source="text", data="")
    invoice_list = [invoice]
    return invoice_list
