from src.type_structure import *
from src.database import Reports
from bs4 import BeautifulSoup
from peewee import DoesNotExist
from weasyprint import HTML
from io import StringIO, BytesIO
import csv
from zipfile import ZipFile, ZIP_DEFLATED
from src.error import *


def export_json_report_v1(report_id: int, owner=None):
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    if report.owner != None and report.owner != owner:
        raise ForbiddenError("You do not have permission to view report")
    
    return Report(**report.to_json())

def export_pdf_report_v1(report_id: int, owner=None) -> bytes:
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    if report.owner != None and report.owner != owner:
        raise ForbiddenError("You do not have permission to view report")
    
    html = export_html_report_v1(report_id)
    pdf_bytes = HTML(string=html).write_pdf()
    
    return pdf_bytes

def copy_element(element, parent):
    new_element = BeautifulSoup(str(element), "lxml").body.contents[0]
    if "hide" in new_element["class"]:
        new_element["class"].remove("hide")
    parent.append(new_element)
    
    return new_element
    
def change_value(soup, tag, id, value):
    soup.find(tag, {"id": str(id)}).string = str(value)

def add_violations(soup, violations, parent):
    failed_rule = soup.find("div", {"name": "failed-rule-template"})
    
    for violation in violations:
        v = copy_element(failed_rule, parent)
        v["name"] = "failed-rule"
        v["class"].append("error" if violation["is_fatal"] else "warning")
        
        v.find("span", {"name": "rule_id"}).string = violation["rule_id"]
        v.find("td", {"name": "desc"}).string = violation["message"]
        if violation["suggestion"]:
            v.find("td", {"name": "suggestion"}).string = violation["suggestion"]
        else:
            v.find("tr", {"id": "suggestion"})["style"] = "display: none;"
            
        v.find("td", {"name": "severity"}).string = "Error" if violation["is_fatal"] else "Warning"
        
        if violation["test"]:
            v.find("code", {"name": "test"}).string = violation["test"]
        else:
            v.find("tr", {"id": "test"})["style"] = "display: none;"
        
        if violation["xpath"]:
            location_string = violation["xpath"]
        else:
            location_string = "Line " + str(violation["line"]) + ", Column " + str(violation["column"])
        v.find("code", {"name": "location"}).string = location_string

def export_html_report_v1(report_id: int, owner=None):
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    if report.owner != None and report.owner != owner:
        raise ForbiddenError("You do not have permission to view report")
    
    report = report.to_json()

    with open("src/report_template.html", "r") as file:
        html = file.read()

    soup = BeautifulSoup(html, "html.parser")

    wellformedness = soup.find("div", {"id": "wellformedness"})
    schema = soup.find("div", {"id": "schema"})
    syntax = soup.find("div", {"id": "syntax"})
    peppol = soup.find("div", {"id": "peppol"})
    no_violation = soup.find("div", {"name": "no-violation"})
    no_run = soup.find("div", {"name": "no-run"})

    change_value(soup, "td", "id-value", report["report_id"])
    change_value(soup, "td", "name-value", report["invoice_name"])
    change_value(soup, "td", "gen-value", report["date_generated"])
    change_value(soup, "td", "hash-value", report["invoice_hash"])
    change_value(soup, "td", "violations-value", report["total_errors"])
    change_value(soup, "td", "warnings-value", report["total_warnings"])

    result = soup.find("td", {"id": "result"})

    if report["is_valid"]:
        result["class"].remove("fail")
        result["class"].append("success")

    if not report["wellformedness_evaluation"]:
        copy_element(no_run, wellformedness)
    elif not report["wellformedness_evaluation"]["violations"]:
        copy_element(no_violation, wellformedness)
    else:
        add_violations(soup, report["wellformedness_evaluation"]["violations"], wellformedness)

    if not report["schema_evaluation"]:
        copy_element(no_run, schema)
    elif not report["schema_evaluation"]["violations"]:
        copy_element(no_violation, schema)
    else:
        add_violations(soup, report["schema_evaluation"]["violations"], schema)
        
    if not report["syntax_evaluation"]:
        copy_element(no_run, syntax)
    elif not report["syntax_evaluation"]["violations"]:
        copy_element(no_violation, syntax)
    else:
        add_violations(soup, report["syntax_evaluation"]["violations"], syntax)
        
    if not report["peppol_evaluation"]:
        copy_element(no_run, peppol)
    elif not report["peppol_evaluation"]["violations"]:
        copy_element(no_violation, peppol)
    else:
        add_violations(soup, report["peppol_evaluation"]["violations"], peppol)

    return str(soup)

def write_violations(writer, violations):
    for violation in violations:
        data = [
            violation["rule_id"],
            "Fatal" if violation["is_fatal"] == "fatal" else "Warning",
            violation["message"],
            violation["test"],
            violation["xpath"],
            violation["line"],
            violation["column"]
        ]
        writer.writerow(data)

def export_csv_report_v1(report_id: int, owner=None):
    if report_id < 0:
        raise InputError(detail="Report id cannot be less than 0")
    
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise NotFoundError(detail=f"Report with id {report_id} not found")
    
    if report.owner != None and report.owner != owner:
        raise ForbiddenError("You do not have permission to view report")
    
    report = report.to_json()
    
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    
    writer.writerow(["Rule ID", "Severity", "Description", "Test", "XPath", "Line", "Column"])
    
    if report["wellformedness_evaluation"]:
        write_violations(writer, report["wellformedness_evaluation"]["violations"])
        
    if report["schema_evaluation"]:
        write_violations(writer, report["schema_evaluation"]["violations"])
        
    if report["syntax_evaluation"]:
        write_violations(writer, report["syntax_evaluation"]["violations"])
        
    if report["peppol_evaluation"]:
        write_violations(writer, report["peppol_evaluation"]["violations"])
    
    csv_contents = csv_buffer.getvalue()
    csv_buffer.close()
    
    return csv_contents

def report_bulk_export_json_v1(report_ids, owner=None) -> ReportList:
    return ReportList(reports=[export_json_report_v1(report_id, owner) for report_id in report_ids])

def report_bulk_export_pdf_v1(report_ids, owner=None) -> BytesIO:
    reports = BytesIO()
    
    with ZipFile(reports, 'w', ZIP_DEFLATED) as f:
        for report_id in report_ids:
            f.writestr(f"invoice_validation_report_{report_id}.pdf", export_pdf_report_v1(report_id, owner))
    
    reports.seek(0)
    
    return reports
