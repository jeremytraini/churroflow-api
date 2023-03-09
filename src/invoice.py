from typing import Dict

from src.types import *
from src.report import report_get_v1

def invoice_quick_fix_wellformedness_v1(report_id: int) -> QuickFixReturn:
    invoice = Invoice(name="My Invoice", format="XML", source="text", data="data")
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
        schemaEvaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = QuickFixReturn (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_quick_fix_syntax_v1(report_id: int) -> QuickFixReturn:
    invoice = Invoice(name="My Invoice", format="XML", source="text", data="data")
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
        schemaEvaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = QuickFixReturn (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_quick_fix_peppol_v1(report_id: int) -> QuickFixReturn:
    invoice = Invoice(name="My Invoice", format="XML", source="text", data="data")
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
        schemaEvaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = QuickFixReturn (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_quick_fix_schema_v1(report_id: int) -> QuickFixReturn:
    invoice = Invoice(name="My Invoice", format="XML", source="text", data="data")
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
        schemaEvaluation=None,
        syntax=None,
        peppol=None
    )
    quick_fix = QuickFixReturn (
        invoice=invoice,
        report=report
    )
    return quick_fix

def invoice_check_validity_v1(report_id: int) -> CheckValidReturn:
    report = report_get_v1(report_id)
    return CheckValidReturn(is_valid=report.is_valid, invoice_hash=report.invoice_hash)

def invoice_generate_hash_v1(invoice: Invoice) -> str:
    return "hash"

def invoice_bulk_quick_fix_v1(invoices: list[Invoice]) -> list[Invoice]:
    invoice = Invoice(name="invoice", format="XML", source="text", data="")
    invoice_list = [invoice]
    return invoice_list
