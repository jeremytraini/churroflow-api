from src.type_structure import *
from src.database import Reports


def export_json_report_v1(report_id: int):
    report = Reports.select().where(report_id==report_id).get()
    
    return report.to_json()

def export_pdf_report_v1(report_id: int):
    pass

def export_html_report_v1(report_id: int):
    pass

def export_csv_report_v1(report_id: int):
    pass

