from src.type_structure import *
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db
from helper_functions import extract_text_from_invoice


def report_wellformedness_v1(invoice: Invoice) -> Evaluation:
    invoice_text = extract_data_from_invoice(invoice)
    evaluation = generate_wellformedness_evaluation(invoice_text)
    
    return evaluation.to_json()

def report_schema_v1(invoice: Invoice) -> Evaluation:
    invoice_text = extract_data_from_invoice(invoice)
    evaluation = generate_schema_evaluation(invoice_text)
    
    return evaluation.as_json()

def report_syntax_v1(invoice: Invoice) -> Evaluation:
    data = extract_data_from_invoice(invoice)
    evaluation = generate_xslt_evaluation("syntax", data, "src/validation_artefacts/AUNZ-UBL-validation.xslt")
    
    return evaluation.as_json()

def report_peppol_v1(invoice: Invoice) -> Evaluation:
    data = extract_data_from_invoice(invoice)
    evaluation = generate_xslt_evaluation("peppol", data, "src/validation_artefacts/AUNZ-PEPPOL-validation.xslt")

    return evaluation.as_json()

def report_get_v1(report_id: int) -> Report:
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
    return report

def report_list_all_v1(order_by: OrderBy) -> List[Report]:
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
    reports = [report]
    return reports

def report_export_v1(report_id, report_format) -> ReportExport:
    export = ReportExport(url="", invoice_hash="")
    return export

def report_change_name_v1(report_id: int, new_name: str) -> Dict[None, None]:
    return {}

def report_delete_v1(report_id: int) -> Dict[None, None]:
    return {}

def report_bulk_generate_v1(invoices: List[Invoice]) -> List[Report]:
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
    reports = [report]
    return reports

def report_bulk_export_v1(report_ids, report_format) -> List[ReportExport]:
    export = ReportExport(url="", invoice_hash="")
    exports = [export]
    return exports

