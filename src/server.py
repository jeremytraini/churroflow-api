import signal
from src.config import base_url, port
from src.health_check import health_check_v1
from src.report import *
from src.invoice import *
from src.types import *
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.error import AuthenticationError, InputError
import uvicorn

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

# ENDPOINTS BELOW

@app.get("/health_check/v1")
async def health_check():
    return health_check_v1()

@app.post("/report/json_report/v1")
async def report_json_report(invoice: Invoice) -> Report:
    return report_json_report_v1(invoice)

# TODO: return type
@app.post("/report/visual_report/v1")
async def report_visual_report(invoice: Invoice, format: Format):
    return report_visual_report_v1(invoice, format)

@app.post("/report/wellformedness/v1")
async def report_wellformedness(invoice: Invoice) -> Evaluation:
    return report_wellformedness_v1(invoice)

@app.post("/report/schema/v1")
async def report_schema(invoice: Invoice) -> Evaluation:
    return report_schema_v1(invoice)

@app.post("/report/syntax/v1")
async def report_syntax(invoice: Invoice) -> Evaluation:
    return report_syntax_v1(invoice)

@app.post("/report/peppol/v1")
async def report_peppol(invoice: Invoice) -> Evaluation:
    return report_peppol_v1(invoice)

@app.get("/report/get/v1")
async def report_get(report_id: int) -> Report:
    return report_get_v1(report_id)

# TODO: discuss changing input type
@app.get("/report/list_all/v1")
async def report_list_all(order_by: str) -> List[Report]:
    return report_list_all_v1(order_by)

# TODO: discuss changing oreder_by type
@app.get("/report/list_score/v1")
async def report_list_score(score: int, order_by: str) -> List[Report]:
    return report_list_score_v1(score, order_by)

# TODO: check format and output types
@app.get("/report/export/v1")
async def report_export(report_id: int, report_format: Format) -> ReportExport:
    return report_export_v1(report_id, report_format)

# TODO: return type
@app.put("/report/change_name/v1")
async def report_change_name(report_id: int, new_name: str) -> Dict[None, None]:
    return report_change_name_v1(report_id, new_name)

# TODO: return type
@app.delete("/report/delete/v1")
async def report_delete(report_id: int) -> Dict[None, None]:
    return report_delete_v1(report_id)

@app.get("/invoice/quick_fix_wellformedness/v1")
async def invoice_quick_fix_wellformedness(report_id: int) -> QuickFixReturn:
    return invoice_quick_fix_wellformedness_v1(report_id)

@app.get("/invoice/quick_fix_syntax/v1")
async def invoice_quick_fix_syntax(report_id: int) -> QuickFixReturn:
    return invoice_quick_fix_syntax_v1(report_id)

@app.get("/invoice/quick_fix_peppol/v1")
async def invoice_quick_fix_peppol(report_id: int) -> QuickFixReturn:
    return invoice_quick_fix_peppol_v1(report_id)

@app.get("/invoice/quick_fix_schema/v1")
async def invoice_quick_fix_schema(report_id: int) -> QuickFixReturn:
    return invoice_quick_fix_schema_v1(report_id)

@app.get("/invoice/check_validity/v1")
async def invoice_check_validity(report_id: int) -> CheckValidReturn:
    return invoice_check_validity_v1(report_id)

@app.post("/invoice/generate_hash/v1")
async def invoice_generate_hash(invoice: Invoice) -> str:
    return invoice_generate_hash_v1(invoice)

# TODO: check return type
@app.post("/report/bulk_generate/v1")
async def report_bulk_generate(invoices: List[Invoice]) -> List[Report]:
    return report_bulk_generate_v1(invoices)

@app.get("/invoice/bulk_quick_fix/v1")
async def invoice_bulk_quick_fix(invoices: List[Invoice]) -> List[Invoice]:
    return invoice_bulk_quick_fix_v1(invoices)

# TODO: check input and return type
@app.get("/report/bulk_export/v1")
async def report_bulk_export(report_ids: List[int], report_format: Format) -> List[ReportExport]:
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
