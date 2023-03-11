from src.type_structure import *
from src.database import Reports
from bs4 import BeautifulSoup
from copy import copy, deepcopy
import json


def export_json_report_v1(report_id: int):
    report = Reports.select().where(report_id==report_id).get()
    
    return report.to_json()

def export_pdf_report_v1(report_id: int):
    pass

def export_html_report_v1(report_id: int):
    report = Reports.select().where(report_id==report_id).get()
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
    failed_rule = soup.find("div", {"name": "failed-rule"})

    def copy_element(element, parent):
        new_element = BeautifulSoup(str(element), "lxml").body.contents[0]
        if "hide" in new_element["class"]:
            new_element["class"].remove("hide")
        parent.append(new_element)
        return new_element

    def change_value(tag, id, value):
        soup.find(tag, {"id": str(id)}).string = str(value)

    change_value("td", "id-value", report["report_id"])
    change_value("td", "name-value", report["invoice_name"])
    change_value("td", "gen-value", report["date_generated"])
    change_value("td", "hash-value", report["invoice_hash"])
    change_value("td", "violations-value", report["total_errors"])
    change_value("td", "warnings-value", report["total_warnings"])
    # change_value("td", "fatal-violations-value", report["total_fatal_violations"])

    result = soup.find("td", {"id": "result"})

    if report["is_valid"]:
        result["class"].remove("fail")
        result["class"].append("success")

    def add_violations(violations, parent):
        for violation in violations:
            v = copy_element(failed_rule, parent)
            v.find("span", {"name": "rule_id"}).string = violation["rule_id"]
            v.find("td", {"name": "desc"}).string = violation["message"]
            v.find("td", {"name": "severity"}).string = "Fatal" if violation["is_fatal"] == "fatal" else "Warning"
            if violation["test"]:
                v.find("code", {"name": "test"}).string = violation["test"]
            else:
                v.find("code", {"name": "test"}).display = "none"
            
            if violation["xpath"]:
                location_string = violation["xpath"]
            else:
                location_string = "Line " + str(violation["line"]) + ", Column " + str(violation["column"])
            v.find("code", {"name": "location"}).string = location_string
            v.find("code", {"name": "excerpt"}).string = ""

    if not report["wellformedness_evaluation"]:
        copy_element(no_run, schema)
    elif not report["wellformedness_evaluation"]["violations"]:
        copy_element(no_violation, wellformedness)
    else:
        add_violations(report["wellformedness_evaluation"]["violations"], wellformedness)

    if not report["schema_evaluation"]:
        copy_element(no_run, schema)
    elif not report["schema_evaluation"]["violations"]:
        copy_element(no_violation, wellformedness)
    else:
        add_violations(report["schema_evaluation"]["violations"], wellformedness)
        
    if not report["syntax_evaluation"]:
        copy_element(no_run, syntax)
    elif not report["syntax_evaluation"]["violations"]:
        copy_element(no_violation, syntax)
    else:
        add_violations(report["syntax_evaluation"]["violations"], syntax)
        
    if not report["peppol_evaluation"]:
        copy_element(no_run, peppol)
    elif not report["peppol_evaluation"]["violations"]:
        copy_element(no_violation, peppol)
    else:
        add_violations(report["peppol_evaluation"]["violations"], peppol)

    # with open("output.html", "w") as file:
    #     file.write(str(soup))



def export_csv_report_v1(report_id: int):
    pass

