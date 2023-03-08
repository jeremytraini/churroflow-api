import signal
from src.config import base_url, port
from src.health_check import health_check_v1
from src.report import report_json_report_v1, report_visual_report_v1, report_wellformedness_v1, report_schema_v1, \
    report_syntax_v1, report_peppol_v1, report_get_v1, report_list_all_v1, report_list_score_v1, report_export_v1, \
    report_change_name_v1, report_delete_v1, report_bulk_generate_v1, report_bulk_export_v1
from src.invoice import invoice_quick_fix_wellformedness_v1, invoice_quick_fix_syntax_v1, invoice_quick_fix_peppol_v1, \
    invoice_quick_fix_schema_v1, invoice_check_validity_v1, invoice_generate_hash_v1, invoice_bulk_quick_fix_v1
from src.report import report_syntax_v1, report_peppol_v1
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.error import AuthenticationError, InputError
import uvicorn
from pydantic import BaseModel

app = FastAPI()

@app.exception_handler(500)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "name": "System Error",
            "message": str(exc)
            },
    )


class Invoice(BaseModel):
    name: str
    format: str
    source: str
    data: str


# ENDPOINTS BELOW

@app.get("/health_check/v1")
async def health_check():
    return health_check_v1()

@app.post("/report/json_report/v1")
async def report_json_report(invoice):
    return report_json_report_v1(invoice)

@app.post("/report/visual_report/v1")
async def report_visual_report(invoice, format):
    return report_visual_report_v1(invoice, format)

@app.post("/report/wellformedness/v1")
async def report_wellformedness(invoice):
    return report_wellformedness_v1(invoice)

@app.post("/report/schema/v1")
async def report_schema(invoice):
    return report_schema_v1(invoice)

@app.post("/report/syntax/v1")
async def report_syntax(invoice: Invoice):
    return report_syntax_v1(invoice.name, invoice.format, invoice.source, invoice.data)


@app.post("/report/peppol/v1")
async def report_peppol(invoice: Invoice):
    return report_peppol_v1(invoice.name, invoice.format, invoice.source, invoice.data)

@app.get("/report/get/v1")
async def report_get(report_id):
    return report_get_v1(report_id)

@app.get("/report/list_all/v1")
async def report_list_all(order_by):
    return report_list_all_v1(order_by)

@app.get("/report/list_score/v1")
async def report_list_score(score, order_by):
    return report_list_score_v1(score, order_by)

@app.get("/report/export/v1")
async def report_export(report_id, report_format):
    return report_export_v1(report_id, report_format)

@app.put("/report/change_name/v1")
async def report_change_name(report_id, new_name):
    return report_change_name_v1(report_id, new_name)

@app.delete("/report/delete/v1")
async def report_delete(report_id):
    return report_delete_v1(report_id)

@app.get("/invoice/quick_fix_wellformedness/v1")
async def invoice_quick_fix_wellformedness(report_id):
    return invoice_quick_fix_wellformedness_v1(report_id)

@app.get("/invoice/quick_fix_syntax/v1")
async def invoice_quick_fix_syntax(report_id):
    return invoice_quick_fix_syntax_v1(report_id)

@app.get("/invoice/quick_fix_peppol/v1")
async def invoice_quick_fix_peppol(report_id):
    return invoice_quick_fix_peppol_v1(report_id)

@app.get("/invoice/quick_fix_schema/v1")
async def invoice_quick_fix_schema(report_id):
    return invoice_quick_fix_schema_v1(report_id)

@app.get("/invoice/check_validity/v1")
async def invoice_check_validity(report_id):
    return invoice_check_validity_v1(report_id)

@app.post("/invoice/generate_hash/v1")
async def invoice_generate_hash(invoice):
    return invoice_generate_hash_v1(invoice)

@app.post("/report/bulk_generate/v1")
async def report_bulk_generate(invoices):
    return report_bulk_generate_v1(invoices)

@app.get("/invoice/bulk_quick_fix/v1")
async def invoice_bulk_quick_fix(invoices):
    return invoice_bulk_quick_fix_v1(invoices)

@app.get("/report/bulk_export/v1")
async def report_bulk_export(report_ids, report_format):
    return report_bulk_export_v1(report_ids, report_format)


# Samples below

@app.post("/test/post/v1")
async def test_post(val: str):
    return val

@app.get("/test/get/v1")
def test_get(val: str):
    return val

@app.put("/test/put/v1")
async def test_put(val: str):
    return val

@app.delete("/test/delete/v1")
async def test_delete(val: str):
    return val

# ENDPOINTS ABOVE

if __name__ == "__main__":
    uvicorn.run(app, host=base_url, port=port)
