from src.type_structure import *


def export_json_report_v1(report_id: int) -> Report:
    report = Reports.query.filter_by(id=report_id).one()
    
    return report.to_json()

def export_pdf_report_v1(report_id: int) -> File():
    report = Reports.query.filter_by(id=report_id).one()

def export_html_report_v1(report_id: int) -> File():
    report = Reports.query.filter_by(id=report_id).one()

def export_csv_report_v1(report_id: int) -> File():
    report = Reports.query.filter_by(id=report_id).one()

