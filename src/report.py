from src.type_structure import *
from typing import Dict
from src.database import Reports, Sessions, Users
from src.generation import generate_xslt_evaluation, generate_schema_evaluation, generate_wellformedness_evaluation
from peewee import DoesNotExist
from src.constants import ADMIN_TOKEN


def report_wellformedness_v1(invoice_text: str) -> Evaluation:
    evaluation = generate_wellformedness_evaluation(invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_schema_v1(invoice_text: str) -> Evaluation:
    evaluation = generate_schema_evaluation(invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_syntax_v1(invoice_text: str) -> Evaluation:
    evaluation = generate_xslt_evaluation("syntax", invoice_text)
    
    return Evaluation(**evaluation.to_json())

def report_peppol_v1(invoice_text: str) -> Evaluation:
    evaluation = generate_xslt_evaluation("peppol", invoice_text)

    return Evaluation(**evaluation.to_json())

def report_list_all_v1() -> ReportIDs:
    return ReportIDs(report_ids=[report.id for report in Reports.select()])

def report_list_by_v1(order_by: OrderBy) -> ReportIDs:
    if order_by.is_ascending:
        order = getattr(Reports, order_by.table).asc()
    else:
        order = getattr(Reports, order_by.table).desc()
    
    return ReportIDs(report_ids=[report.id for report in Reports.select().order_by(order)])

def report_change_name_v2(token: str, report_id: int, new_name: str) -> Dict[None, None]:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    if not token == ADMIN_TOKEN:
        try:
            session =  Sessions.get(token=token)
        except DoesNotExist:
            raise Exception("Invalid token")
        if not report.owner == session.user:
            raise Exception("You do not have permission to rename this report")
    
    report.invoice_name = new_name
    report.save()
    
    return {}

def report_delete_v2(token: str, report_id: int) -> Dict[None, None]:
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")

    if not token == ADMIN_TOKEN:
        try:
            session =  Sessions.get(token=token)
        except DoesNotExist:
            raise Exception("Invalid API key")
        
        if not report.owner == session.user:
            raise Exception("You do not have permission to delete this report")
    
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

