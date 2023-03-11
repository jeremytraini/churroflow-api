from src.type_structure import *
from src.database import Reports
from bs4 import BeautifulSoup
from copy import copy, deepcopy
import json
from html import escape
from peewee import DoesNotExist
from src.server import HTTPException


def export_json_report_v1(report_id: int):
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
    return report.to_json()

def export_pdf_report_v1(report_id: int):
    pass

def copy_element(element, parent):
    new_element = BeautifulSoup(str(element), "lxml").body.contents[0]
    if "hide" in new_element["class"]:
        new_element["class"].remove("hide")
    parent.append(new_element)
    
    return new_element
    
def change_value(soup, tag, id, value):
    soup.find(tag, {"id": str(id)}).string = escape(str(value))

def add_violations(soup, violations, parent):
    failed_rule = soup.find("div", {"name": "failed-rule"})
    
    for violation in violations:
        v = copy_element(failed_rule, parent)
        v.find("span", {"name": "rule_id"}).string = escape(violation["rule_id"])
        v.find("td", {"name": "desc"}).string = escape(violation["message"])
        v.find("td", {"name": "severity"}).string = "Fatal" if violation["is_fatal"] == "fatal" else "Warning"
        if violation["test"]:
            v.find("code", {"name": "test"}).string = violation["test"]
        else:
            v.find("code", {"name": "test"}).display = "none"
        
        if violation["xpath"]:
            location_string = violation["xpath"]
        else:
            location_string = "Line " + str(violation["line"]) + ", Column " + str(violation["column"])
        v.find("code", {"name": "location"}).string = escape(location_string)
        v.find("code", {"name": "excerpt"}).string = ""

def export_html_report_v1(report_id: int):
    try:
        report = Reports.get_by_id(report_id)
    except DoesNotExist:
        raise Exception(f"Report with id {report_id} not found")
    
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



def export_csv_report_v1(report_id: int):
    pass

