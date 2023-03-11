import signal
from src.config import base_url, port
from src.health_check import health_check_v1
from src.report import *
from src.invoice import *
from src.export import *
from src.type_structure import *
from src.database import clear_v1
from fastapi import FastAPI, Request, HTTPException, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
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

@app.post("/invoice/upload_text/v1")
async def invoice_upload_text(invoice_name: str, invoice_text: str) -> Dict:
    return invoice_upload_text_v1(invoice_name=invoice_name, invoice_text=invoice_text)

@app.post("/invoice/upload_url/v1")
async def invoice_upload_url(invoice_name: str, invoice_url: str) -> Dict:
    return invoice_upload_url_v1(invoice_name=invoice_name, invoice_url=invoice_url)

@app.post("/invoice/upload_file/v1")
async def invoice_upload_file(invoice_file: UploadFile) -> Dict:
    return invoice_upload_file_v1(invoice_name=invoice_file.filename, invoice_file=invoice_file.file)

@app.get("/export/json_report/v1")
async def export_json_report(report_id: int):
    return export_json_report_v1(report_id)

@app.get("/export/pdf_report/v1")
async def export_pdf_report(report_id: int):
    return export_pdf_report_v1(report_id)

@app.get("/export/html_report/v1", response_class=HTMLResponse)
async def export_html_report(report_id: int):
    html_content = export_html_report_v1(report_id)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/export/csv_report/v1")
async def export_csv_report(report_id: int):
    return export_csv_report_v1(report_id)

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

@app.get("/report/list_all/v1")
async def report_list_all(order_by: OrderBy) -> List[Report]:
    return report_list_all_v1(order_by)

@app.get("/report/list_score/v1")
async def report_list_score(score: int, order_by: OrderBy) -> List[Report]:
    return report_list_score_v1(score, order_by)

# TODO: return type
@app.put("/report/change_name/v1")
async def report_change_name(report_id: int, new_name: str) -> Dict[None, None]:
    return report_change_name_v1(report_id, new_name)

# TODO: return type
@app.delete("/report/delete/v1")
async def report_delete(report_id: int) -> Dict[None, None]:
    return report_delete_v1(report_id)

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


@app.delete("/clear/v1")
async def clear():
    return clear_v1()


# ENDPOINTS ABOVE

if __name__ == "__main__":
    uvicorn.run(app, host=base_url, port=port)
