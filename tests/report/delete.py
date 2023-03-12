from src.type_structure import *
from tests.server_calls import report_delete_v1
from tests.constants import VALID_INVOICE_TEXT
from tests.helpers import invalidate_invoice, remove_part_of_string

"""
=====================================
/report/delete/v1 TESTS
=====================================
"""

def test_delete():
    report_id = invoice_upload_text_v1("invoice", VALID_INVOICE_TEXT)["report_id"]
    
    report_delete_v1(report_id)
    
    assert export_json_report_v1(report_ids[0])["code"] == 500
