import signal
from src.config import base_url, port
from src.health_check import health_check_v1
from src.report import *
from src.invoice import *
from src.export import *
from src.authentication import *
from src.type_structure import *
from src.database import clear_v1
from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import Response, JSONResponse, HTMLResponse, StreamingResponse
from src.error import AuthenticationError, InputError
from io import BytesIO
import uvicorn


description = """
CHURROS VALIDATION API helps you validate **any** invoice! 🚀🚀
"""

tags_metadata = [
    {
        "name": "invoice",
        "description": "Uploading invoices to the API and generating reports."
    },
    {
        "name": "export",
        "description": "Exporting reports to JSON, PDF, HTML or CSV."
    },
    {
        "name": "report",
        "description": "Generate individual evaluations and manage your reports."
    },
]

app = FastAPI(title="CHURROS VALIDATION API",
              description=description,
              version="0.0.1",
              openapi_tags=tags_metadata)

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

@app.post("/invoice/upload_file/v1", tags=["invoice"])
async def invoice_upload_file(file: UploadFile = File(...)) -> ReportID:
    invoice_text = await file.read()
    return invoice_upload_file_v1(invoice_name=file.filename, invoice_text=invoice_text.decode("utf-8")) #type: ignore

@app.post("/invoice/bulk_upload_file/v1", tags=["invoice"])
async def invoice_bulk_upload_file(files: List[UploadFile] = File(...)) -> ReportIDs:
    invoices = []
    
    for file in files:
        invoice_text = await file.read()
        invoice = TextInvoice(name=file.filename, text=invoice_text.decode("utf-8")) #type: ignore
        invoices.append(invoice)
    
    return invoice_upload_bulk_text_v1(invoices)

@app.post("/invoice/upload_text/v1", tags=["invoice"])
async def invoice_upload_text(invoice: TextInvoice) -> ReportID:
    return invoice_upload_text_v1(invoice_name=invoice.name, invoice_text=invoice.text)

@app.post("/invoice/bulk_upload_text/v1", tags=["invoice"])
async def invoice_upload_bulk_text(invoices: List[TextInvoice]) -> ReportIDs:
    return invoice_upload_bulk_text_v1(invoices)

@app.post("/invoice/upload_url/v1", tags=["invoice"])
async def invoice_upload_url(invoice: RemoteInvoice) -> ReportID:
    return invoice_upload_url_v1(invoice_name=invoice.name, invoice_url=invoice.url)

@app.get("/export/json_report/v1", tags=["export"])
async def export_json_report(report_id: int) -> Report:
    return export_json_report_v1(report_id)

@app.post("/export/bulk_json_reports/v1", tags=["export"])
async def report_bulk_export_json(report_ids: List[int]) -> ReportList:
    return report_bulk_export_json_v1(report_ids)

@app.get("/export/pdf_report/v1", tags=["export"])
async def export_pdf_report(report_id: int) -> StreamingResponse:
    pdf_file = BytesIO(export_pdf_report_v1(report_id))

    # Return the PDF as a streaming response
    headers = {
        "Content-Disposition": f"attachment; filename=invoice_validation_report_{report_id}.pdf",
        "Content-Type": "application/pdf",
    }
    return StreamingResponse(pdf_file, headers=headers)

@app.post("/export/bulk_pdf_reports/v1", tags=["export"])
async def report_bulk_export_pdf(report_ids: List[int]) -> StreamingResponse:
    reports_zip = report_bulk_export_pdf_v1(report_ids)
    
    return StreamingResponse(
        reports_zip, 
        media_type="application/x-zip-compressed", 
        headers = { "Content-Disposition": f"attachment; filename=reports.zip"}
    )

@app.get("/export/html_report/v1", response_class=HTMLResponse, tags=["export"])
async def export_html_report(report_id: int) -> HTMLResponse:
    html_content = export_html_report_v1(report_id)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/export/csv_report/v1", tags=["export"])
async def export_csv_report(report_id: int) -> HTMLResponse:
    csv_contents = export_csv_report_v1(report_id)
    
    response = HTMLResponse(content=csv_contents, media_type='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename="invoice_validation_report_{report_id}.csv"'

    return response

@app.post("/report/wellformedness/v1", tags=["report"])
async def report_wellformedness(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_wellformedness_v1(invoice_text=invoice_text.decode("utf-8"))

@app.post("/report/schema/v1", tags=["report"])
async def report_schema(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_schema_v1(invoice_text=invoice_text.decode("utf-8"))

@app.post("/report/syntax/v1", tags=["report"])
async def report_syntax(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_syntax_v1(invoice_text=invoice_text.decode("utf-8"))

@app.post("/report/peppol/v1", tags=["report"])
async def report_peppol(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_peppol_v1(invoice_text=invoice_text.decode("utf-8"))

@app.get("/report/list_all/v1", tags=["report"])
async def report_list_all() -> ReportIDs:
    return report_list_all_v1()

@app.get("/report/list_by/v1", tags=["report"])
async def report_list_by(order_by: OrderBy) -> ReportIDs:
    return report_list_by_v1(order_by)

@app.get("/report/check_validity/v1", tags=["report"])
async def invoice_check_validity(report_id: int) -> CheckValidReturn:
    return invoice_check_validity_v1(report_id)


### Below to be replaced with proper authentication system ###

@app.put("/report/change_name/v2", include_in_schema=False)
async def report_change_name(token: str, report_id: int, new_name: str) -> Dict[None, None]:
    return report_change_name_v1(token, report_id, new_name)

@app.delete("/report/delete/v2", include_in_schema=False)
async def report_delete(token: str, report_id: int) -> Dict[None, None]:
    return report_delete_v1(token, report_id)

# TODO: check if we should still keep this
# @app.get("/auth_login/v2", include_in_schema=False)
# async def auth_login(email: str, password: str):
#     return auth_login_v1(email, password)

# @app.get("/auth_register/v2", include_in_schema=False)
# async def auth_register(email: str, password: str):
#     return auth_register_v1(email, password)

@app.get("/auth_login/v2", include_in_schema=False)
async def auth_login(email: str, password: str) -> AuthReturnV2:
    return auth_login_v2(email, password)

@app.get("/auth_register/v2", include_in_schema=False)
async def auth_register(email: str, password: str) -> AuthReturnV2:
    return auth_register_v2(email, password)

@app.post("/invoice/generate_hash/v2", include_in_schema=False)
async def invoice_generate_hash(invoice_text: TextInvoice) -> str:
    return invoice_generate_hash_v1(invoice_text)

@app.delete("/clear/v1", include_in_schema=False)
async def clear(token: str):
    return clear_v1(token)


# ENDPOINTS ABOVE

if __name__ == "__main__":
    uvicorn.run(app, host=base_url, port=port)
