from src.type_structure import *
from typing import Dict
from src.database import Reports
from src.generation import generate_xslt_evaluation, generate_schema_evaluation, generate_wellformedness_evaluation, generate_diagnostic_list
from peewee import DoesNotExist
from src.constants import ADMIN_TOKEN, PEPPOL_EXECUTABLE, SYNTAX_EXECUTABLE
from src.error import *


def report_wellformedness_v1(invoice_text: str) -> Evaluation:
    evaluation = generate_wellformedness_evaluation(invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_schema_v1(invoice_text: str) -> Evaluation:
    if not report_wellformedness_v1(invoice_text).is_valid:
        raise InputError(detail="Invoice is not wellformed")
    
    evaluation = generate_schema_evaluation(invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_syntax_v1(invoice_text: str) -> Evaluation:
    if not report_wellformedness_v1(invoice_text).is_valid:
        raise InputError(detail="Invoice is not wellformed")
    
    evaluation = generate_xslt_evaluation(SYNTAX_EXECUTABLE, invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_peppol_v1(invoice_text: str) -> Evaluation:
    if not report_wellformedness_v1(invoice_text).is_valid:
        raise InputError(detail="Invoice is not wellformed")
    
    evaluation = generate_xslt_evaluation(PEPPOL_EXECUTABLE, invoice_text)

    return Evaluation(**evaluation.to_json())

def report_list_all_v1() -> List[int]:
    return ReportIDs(report_ids=[report.id for report in Reports.select()])

def report_list_by_v1(order_by: OrderBy) -> List[int]:
    if order_by.is_ascending:
        order = getattr(Reports, order_by.table).asc()
    else:
        order = getattr(Reports, order_by.table).desc()
    
    return ReportIDs(report_ids=[report.id for report in Reports.select().order_by(order)])

def report_change_name_v1(token: str, report_id: int, new_name: str) -> Dict[None, None]:
    if len(new_name) > 100:
        raise InputError(detail="New name is longer than 100 characters")
    
    if not token == ADMIN_TOKEN:
        raise InputError(detail="Only admins can change the names of reports at the moment")
    
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    report.invoice_name = new_name
    report.save()
    
    return {}

def report_delete_v1(token: str, report_id: int) -> Dict[None, None]:
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    if not token == ADMIN_TOKEN:
        raise InputError(detail="Only admins can change the names of reports at the moment")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    report.delete_instance()
    
    return {}

def report_bulk_generate_v1(invoices: List[TextInvoice]) -> List[Report]:
    report = Report(
        report_id=0,
        date_generated="",
        invoice_name="",
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

def report_bulk_json_export_v1(report_ids) -> List[ReportExport]:
    export = ReportExport(url="", invoice_hash="")
    exports = [export for _ in report_ids]
    return exports

def report_lint_v1(invoice_text: str) -> LintReport:
    return LintReport(
        report=generate_diagnostic_list(invoice_text)
    )

