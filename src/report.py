from src.type_structure import *
from lxml import etree
from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests
from os import unlink
from src.database import Users, Reports, Violations, Evaluations, db


def report_json_report_v1(invoice: Invoice) -> Report:
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
    return report

def report_visual_report_v1(invoice: Invoice, format: Format) -> Dict:
    return {}

def report_wellformedness_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="wellformedness",
        is_valid=True,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )

    data = extract_data_from_invoice(invoice)

    try:
        etree.fromstring(data.encode("utf-8"), parser=None)
    except etree.XMLSyntaxError as error:
        evaluation.is_valid = False
        evaluation.num_rules_failed = 1
        evaluation.num_violations = 1
        violation = Violation(
            rule_id="wellformedness",
            is_fatal=True,
            line=error.lineno,
            column=error.offset,
            test="",
            message=error.msg,
            suggestion="suggestion"
        )
        evaluation.violations.append(violation)

    return evaluation

def report_schema_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="schema",
        is_valid=True,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    
    data = extract_data_from_invoice(invoice)

    # TODO: can probably do this outside the function so that it isn't repeated
    # Parse the XSD file
    xsd_doc = etree.parse("src/xsd/maindoc/UBL-Invoice-2.1.xsd", parser=None)
    xsd = etree.XMLSchema(xsd_doc)
    # Parse the XML data
    xml_doc = etree.fromstring(data.encode("utf-8"), parser=None)
    # Validate the XML against the XSD schema
    is_valid = xsd.validate(xml_doc)
    print(is_valid)
    if not is_valid:
        print('Not valid! :(')
        evaluation.is_valid = False
        errors = []
        for error in xsd.error_log:
            errors.append(error)
            evaluation.violations.append(
                Violation(
                    rule_id="wellformedness",
                    is_fatal=True,
                    line=error.lineno,
                    column=error.offset,
                    test="",
                    message=error.msg,
                    suggestion="suggestion"
                )
            )
            evaluation.num_rules_failed += not (error in errors)
            print(error.message)
            print()
    
    evaluation.num_violations = len(evaluation.violations)
    
    return evaluation

def report_json_report_v1(invoice: Invoice) -> Report:
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

def report_syntax_v1(invoice: Invoice) -> Evaluation:
    data = extract_data_from_invoice(invoice)
    return generate_xslt_evaluation("syntax", data, "src/validation_artefacts/AUNZ-UBL-validation.xslt")

def report_peppol_v1(invoice: Invoice) -> Evaluation:
    data = extract_data_from_invoice(invoice)
    return generate_xslt_evaluation("peppol", data, "src/validation_artefacts/AUNZ-PEPPOL-validation.xslt")

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

def report_list_score_v1(score: int, order_by: OrderBy) -> List[Report]:
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

def extract_data_from_invoice(invoice: Invoice) -> str:
    if invoice.source == "url":
        response = requests.get(invoice.data)
        if response.status_code != 200:
            raise Exception("Could not retrieve file from url")

        data = response.text
    elif invoice.source == "text":
        data = invoice.data
    else:
        raise Exception("Invalid source, please enter url or text")

    return data
