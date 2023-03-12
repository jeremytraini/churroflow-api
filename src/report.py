from src.type_structure import *
from typing import Dict
from tempfile import NamedTemporaryFile
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db
from src.helpers import extract_text_from_invoice
from src.generation import generate_xslt_evaluation, generate_schema_evaluation, generate_wellformedness_evaluation


def report_wellformedness_v1(invoice: Invoice) -> Evaluation:
    invoice_text = extract_text_from_invoice(invoice)
    evaluation = generate_wellformedness_evaluation(invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_schema_v1(invoice: Invoice) -> Evaluation:
    invoice_text = extract_text_from_invoice(invoice)
    evaluation = generate_schema_evaluation(invoice_text)
    
    return Evaluation(**evaluation.to_json())
def report_syntax_v1(invoice: Invoice) -> Evaluation:
    data = extract_text_from_invoice(invoice)
    evaluation = generate_xslt_evaluation("syntax", data)
    
    return Evaluation(**evaluation.to_json())
def report_peppol_v1(invoice: Invoice) -> Evaluation:
    data = extract_text_from_invoice(invoice)
    evaluation = generate_xslt_evaluation("peppol", data)

    return Evaluation(**evaluation.to_json())

def report_list_all_v1() -> List[int]:
    return [report.id for report in Reports.select()]

def report_list_by_v1(order_by: OrderBy) -> List[int]:
    if order_by.is_ascending:
        order = getattr(Reports, order_by.table).asc()
    else:
        order = getattr(Reports, order_by.table).desc()
    
    return [report.id for report in Reports.select().order_by(order)]

def report_change_name_v1(report_id: int, new_name: str) -> Dict[None, None]:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    report.invoice_name = new_name
    report.save()
    
    return {}

def report_delete_v1(report_id: int) -> Dict[None, None]:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    report.delete_instance()
    
    return {}

def report_bulk_generate_v1(invoices: List[Invoice]) -> List[Report]:
    report = Report(
        report_id=0,
        date_generated="",
        invoice_name="",
        invoice_text="",
        invoice_hash="",
        is_valid=True,
        total_warnings=0,
        total_errors=0,
        wellformedness_evaluation=None,
        schema_evaluation=None,
        syntax_evaluation=None,
        peppol_evaluation=None
    )
    reports = [report]
    return reports
