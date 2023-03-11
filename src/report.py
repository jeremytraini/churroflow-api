from src.types import *
from lxml import etree
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
        schema_evaluation=None,
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
        num_rules_fired=0,
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
        evaluation.violations.append(
            Violation(
                rule_id="wellformedness",
                is_fatal=True,
                location=Location(
                    type="line",
                    line=error.lineno,
                    column=error.offset
                ),
                test="",
                message=error.msg,
                suggestion="suggestion"
            )
        )

    return evaluation

def report_schema_v1(invoice: Invoice) -> Evaluation:
    evaluation = Evaluation(
        aspect="schema",
        is_valid=True,
        num_rules_fired=0,
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
    if not is_valid:
        evaluation.is_valid = False
        error_types = []
        for error in xsd.error_log:
            evaluation.violations.append(
                Violation(
                    rule_id=error.type,
                    is_fatal=True,
                    location=Location(
                        type="line",
                        line=error.line,
                        column=error.column
                    ),
                    test=error.type_name,
                    message=error.message,
                    suggestion="suggestion"
                )
            )
            evaluation.num_rules_failed += not (error.type in error_types)
            error_types.append(error.type)
    
    evaluation.num_violations = len(evaluation.violations)
    
    return evaluation

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

def report_list_all_v1(order_by: Order_By) -> List[Report]:
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

def report_list_score_v1(score: int, order_by: Order_By) -> List[Report]:
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

# Helper functions

def generate_xslt_evaluation(aspect, invoice_text, xslt_path) -> Evaluation:
    with PySaxonProcessor(license=False) as proc:
        
        xsltproc = proc.new_xslt30_processor()
        executable = xsltproc.compile_stylesheet(stylesheet_file=xslt_path)
        
        if xsltproc.exception_occurred:
            raise Exception("XSLT failed to load! " + xsltproc.error_message)
        
        if executable.exception_occurred:
            raise Exception("Executable failed to load! " + executable.error_message)
        
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
            aspect=aspect,
            is_valid=is_valid,
            num_rules_fired=len(output),
            num_rules_failed=len(rules_failed),
            num_violations=len(violations),
            violations=violations
        )
        
        return result

def extract_data_from_invoice(invoice: Invoice) -> str:
    if invoice.source == "file":
        with open(invoice.data, 'r') as f:
            data = f.read()
    elif invoice.source == "url":
        response = requests.get(invoice.data)
        if response.status_code != 200:
            raise Exception("Could not retrieve file from url")

        data = response.text
    elif invoice.source == "text":
        data = invoice.data
    else:
        raise Exception("Invalid Source")

    return data
