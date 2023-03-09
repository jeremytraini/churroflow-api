from src.classes.Validator_lxml import Validator
from src.types import *
from typing import Dict
from saxonche import PySaxonProcessor
from tempfile import NamedTemporaryFile
import requests

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

# wellformedness report stub
def report_wellformedness_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="wellformedness",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    # model of evaluation with one violation
    # evaluation = Evaluation(
    #     aspect="wellformedness",
    #     is_valid=True,
    #     num_rules_fired=0,
    #     num_rules_failed=1,
    #     num_violations=1,
    #     violations=[Violation(
    #         rule_id="wellformedness",
    #         is_fatal=True,
    #         location=LocationLine(
    #             line=1,
    #             column=1
    #         ),
    #         test="test",
    #         message="message",
    #         suggestion="suggestion"
    #     )]
    # )
    return evaluation

# schema report stub
def report_schema_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="schema",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    validator = Validator("src/validation_artefacts/UBL-Invoice-2.1.xsd")

    # The directory with XML files
    file_path = "test/example_files/AUInvoice_valid.xml"
    
    if validator.validate(file_path):
        print('Valid! :)')
    else:
        evaluation.is_valid = False
        print('Not valid! :(')
    return evaluation

# Syntax report stub
def report_syntax_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="syntax",
        is_valid=True,
        num_rules_fired=0,
        num_rules_failed=0,
        num_violations=0,
        violations=[]
    )
    return evaluation

def report_peppol_v1(invoice: Invoice) -> Evaluation:
    if invoice.source == "file":
        with open(invoice.data, 'r') as f:
            data = f.read()
    elif invoice.source == "url":
        response = requests.get(invoice.data)
        if response.status_code != 200:
            raise Exception("Could not retrieve file from url")

        data = response.text
    
    return generate_xslt_evaluation(invoice.data, "src/validation_artefacts/AUNZ-PEPPOL-validation.xslt")

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
        schemaEvaluation=None,
        syntax=None,
        peppol=None
    )
    return report

# TODO: test
def report_list_all_v1(order_by: str) -> list[Report]:
    (order, asc) = order_by.split(" ")
    print(order)
    print(asc)
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
    reports = [report]
    return reports

def report_list_score_v1(score: int, order_by: str) -> list[Report]:
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
    reports = [report]
    return reports

def report_export_v1(report_id, report_format) -> ReportExport:
    export = ReportExport(url="", invoice_hash="")
    return export

def report_change_name_v1(report_id: int, new_name: str) -> Dict[None, None]:
    return {}

def report_delete_v1(report_id: int) -> Dict[None, None]:
    return {}

def report_bulk_generate_v1(invoices: list[Invoice]) -> list[Report]:
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
    reports = [report]
    return reports

def report_bulk_export_v1(report_ids, report_format) -> list[ReportExport]:
    export = ReportExport(url="", invoice_hash="")
    exports = [export]
    return exports

# Helper functions

def generate_xslt_evaluation(invoice_text, xslt_path) -> Evaluation:
    with PySaxonProcessor(license=False) as proc:
        
        print(xslt_path)
        
        xsltproc = proc.new_xslt30_processor()
        executable = xsltproc.compile_stylesheet(stylesheet_file=xslt_path)
        
        if xsltproc.exception_occurred:
            raise Exception("XSLT failed to load! " + xsltproc.error_message)
        
        if executable.exception_occurred:
            raise Exception("Executable failed to load! " + executable.error_message)
        
        print(len(invoice_text))
        
        tmp = NamedTemporaryFile(mode='w', delete=False)
        tmp.write(invoice_text)
        tmp.close()
        
        schematron_output = executable.transform_to_value(source_file=tmp.name)
        
        if not schematron_output:
            raise Exception("Schematron output is empty")
        
        violations = []
        is_valid = True
        rules_failed = set()
        
        output = schematron_output.item_at(0).get_node_value().children[0].children
        
        for item in output:
            if item.name and item.name.endswith("failed-assert"):
                id_name = item.get_attribute_value("id")
                rules_failed.add(id_name)
                is_fatal = item.get_attribute_value("flag") == "fatal"
                
                if is_valid and is_fatal:
                    is_valid = False
                
                location = item.get_attribute_value("location")
                test = item.get_attribute_value("test")
                message = ""
                if item.children:
                    message = item.children[0].string_value
                suggestion = ""
                if len(item.children) > 1:
                    suggestion = item.children[1].string_value
                
                violations.append({
                    "rule_id": id_name,
                    "is_fatal": is_fatal,
                    "location": {
                                    "type": "xpath",
                                    "xpath": location
                                    },
                    "test": test,
                    "message": message,
                    "suggestion": suggestion
                })
        
        result =  Evaluation(
            aspect="peppol",
            is_valid=is_valid,
            num_rules_fired=len(output),
            num_rules_failed=len(rules_failed),
            num_violations=len(violations),
            violations=violations
        )
        
        return result
