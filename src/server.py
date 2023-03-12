import signal
from src.config import base_url, port
from src.health_check import health_check_v1
from src.report import *
from src.invoice import *
from src.export import *
from src.type_structure import *
from src.database import clear_v1
from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import Response, JSONResponse, HTMLResponse, StreamingResponse
from src.error import AuthenticationError, InputError
from io import BytesIO
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

@app.get("/")
async def welcome():
    return "Welcome to the Churros Validation API!"

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
async def invoice_upload_file(file: UploadFile = File(...)) -> Dict:
    file_data = await file.read()
    return invoice_upload_file_v1(invoice_name=file.filename, invoice_file=file_data) # type: ignore

@app.get("/export/json_report/v1")
async def export_json_report(report_id: int):
    return export_json_report_v1(report_id)

@app.get("/export/pdf_report/v1")
async def export_pdf_report(report_id: int):
    pdf_file = BytesIO(export_pdf_report_v1(report_id)) # type: ignore

    # Return the PDF as a streaming response
    headers = {
        "Content-Disposition": f"attachment; filename=invoice_validation_report_{report_id}.pdf",
        "Content-Type": "application/pdf",
    }
    return StreamingResponse(pdf_file, headers=headers)

@app.get("/export/html_report/v1", response_class=HTMLResponse)
async def export_html_report(report_id: int):
    html_content = export_html_report_v1(report_id)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/export/csv_report/v1")
async def export_csv_report(report_id: int):
    csv_contents = export_csv_report_v1(report_id)
    
    response = Response(content=csv_contents, media_type='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename="invoice_validation_report_{report_id}.csv"'

    return response

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

@app.get("/report/list_all/v1")
async def report_list_all() -> List[int]:
    return report_list_all_v1()

@app.get("/report/list_by/v1")
async def report_list_by(order_by: OrderBy) -> List[int]:
    return report_list_by_v1(order_by)

@app.put("/report/change_name/v1")
async def report_change_name(report_id: int, new_name: str) -> Dict[None, None]:
    return report_change_name_v1(report_id, new_name)

@app.delete("/report/delete/v1")
async def report_delete(report_id: int) -> Dict[None, None]:
    return report_delete_v1(report_id)

@app.get("/report/check_validity/v1")
async def invoice_check_validity(report_id: int) -> CheckValidReturn:
    return invoice_check_validity_v1(report_id)

@app.post("/invoice/generate_hash/v1")
async def invoice_generate_hash(invoice: Invoice) -> str:
    return invoice_generate_hash_v1(invoice)

@app.post("/invoice/file_upload_bulk/v1")
async def invoice_file_upload_bulk(invoices: List[Invoice]) -> List[int]:
    return invoice_file_upload_bulk_v1(invoices)

@app.post("/report/bulk_export/v1")
async def report_bulk_export(report_ids: List[int], report_format: str) -> List[str]:
    return report_bulk_export_v1(report_ids, report_format)


@app.delete("/clear/v1")
async def clear():
    return clear_v1()


# ENDPOINTS ABOVE

if __name__ == "__main__":
    uvicorn.run(app, host=base_url, port=port)
