from src.config import base_url, port
from src.health_check import health_check_v1
from src.report import *
from src.invoice import *
from src.export import *
from src.send_email_report import *
from src.authentication import *
from src.invoice_processing import *
from src.type_structure import *
from src.responses import *
from src.database import clear_v2
from src.kmeans import *
from fastapi import Depends, FastAPI, Request, UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from fastapi.responses import JSONResponse, HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(InputError)
async def input_error_exception_handler(request: Request, exc: InputError):
    return JSONResponse(
        status_code=400,
        content={
            "code": 400,
            "name": "Input Error",
            "detail": exc.detail
        },
    )

@app.exception_handler(UnauthorisedError)
async def authorization_error_exception_handler(request: Request, exc: UnauthorisedError):
    return JSONResponse(
        status_code=401,
        content={
            "code": 401,
            "name": "Unauthorised Error",
            "detail": exc.detail
        },
    )

@app.exception_handler(ForbiddenError)
async def forbidden_error_exception_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=403,
        content={
            "code": 403,
            "name": "Forbidden Error",
            "detail": exc.detail
        },
    )

@app.exception_handler(NotFoundError)
async def not_found_error_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "code": 404,
            "name": "Not Found Error",
            "detail": exc.detail
        },
    )

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "name": "Internal Server Error",
            "detail": str(exc)
        },
    )

# token validation below

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth_login/v2")

async def get_token(token: str = Depends(oauth2_scheme)) -> str:
    try:
        session = Sessions.get(token=token)
    except DoesNotExist:
        raise UnauthorisedError("Invalid token, please login/register")
    
    if session.date_expires < datetime.now():
        raise UnauthorisedError("Expired token, please login again")

    return session.token

# ENDPOINTS BELOW

@app.get("/")
async def welcome():
    return "Welcome to the Churros Validation API!"

@app.get("/health_check/v1")
async def health_check():
    return health_check_v1()

# V1 INVOICE ENDPOINTS

@app.post("/invoice/upload_file/v1", tags=["invoice"], responses=res_invoice_upload_file_v1)
async def invoice_upload_file(file: UploadFile = File(...)) -> ReportID:
    invoice_text = await file.read()
    return invoice_upload_file_v1(invoice_name=file.filename, invoice_text=invoice_text.decode("utf-8")) #type: ignore

@app.post("/invoice/bulk_upload_file/v1", tags=["invoice"], responses=res_invoice_bulk_upload_file_v1)
async def invoice_bulk_upload_file(files: List[UploadFile] = File(...)) -> ReportIDs:
    invoices = []
    
    for file in files:
        invoice_text = await file.read()
        invoice = TextInvoice(name=file.filename, text=invoice_text.decode("utf-8")) #type: ignore
        invoices.append(invoice)
    
    return invoice_upload_bulk_text_v1(invoices)



@app.post("/invoice/upload_text/v1", tags=["invoice"], responses=res_invoice_upload_text_v1)
async def invoice_upload_text(invoice: TextInvoice) -> ReportID:
    return invoice_upload_text_v1(invoice_name=invoice.name, invoice_text=invoice.text)

@app.post("/invoice/bulk_upload_text/v1", tags=["invoice"], responses=res_invoice_bulk_upload_text_v1)
async def invoice_upload_bulk_text(invoices: List[TextInvoice]) -> ReportIDs:
    return invoice_upload_bulk_text_v1(invoices)


@app.post("/invoice/upload_url/v1", tags=["invoice"], responses=res_invoice_upload_url_v1)
async def invoice_upload_url(invoice: RemoteInvoice) -> ReportID:
    return invoice_upload_url_v1(invoice_name=invoice.name, invoice_url=invoice.url)


# EXPORT ENDPOINTS

@app.get("/export/json_report/v1", tags=["export"], responses=res_export_json_report_v1)
async def export_json_report(report_id: int) -> Report:
    return export_json_report_v1(report_id)


@app.post("/export/bulk_json_reports/v1", tags=["export"], responses=res_export_bulk_json_report_v1)
async def report_bulk_export_json(report_ids: List[int]) -> ReportList:
    return report_bulk_export_json_v1(report_ids)

@app.get("/export/pdf_report/v1", tags=["export"], responses=res_export_pdf_report_v1)
async def export_pdf_report(report_id: int) -> StreamingResponse:
    pdf_file = BytesIO(export_pdf_report_v1(report_id))

    # Return the PDF as a streaming response
    headers = {
        "Content-Disposition": f"attachment; filename=invoice_validation_report_{report_id}.pdf",
        "Content-Type": "application/pdf",
    }
    return StreamingResponse(pdf_file, headers=headers)

@app.post("/export/bulk_pdf_reports/v1", tags=["export"], responses=res_export_bulk_pdf_report_v1)
async def report_bulk_export_pdf(report_ids: List[int]) -> StreamingResponse:
    reports_zip = report_bulk_export_pdf_v1(report_ids)
    
    return StreamingResponse(
        reports_zip, 
        media_type="application/x-zip-compressed", 
        headers = { "Content-Disposition": f"attachment; filename=reports.zip"}
    )

@app.get("/export/html_report/v1", response_class=HTMLResponse, tags=["export"], responses=res_export_html_report_v1)
async def export_html_report(report_id: int) -> HTMLResponse:
    html_content = export_html_report_v1(report_id)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/export/csv_report/v1", tags=["export"], responses=res_export_csv_report_v1)
async def export_csv_report(report_id: int) -> HTMLResponse:
    csv_contents = export_csv_report_v1(report_id)
    
    response = HTMLResponse(content=csv_contents, media_type='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename="invoice_validation_report_{report_id}.csv"'

    return response

# REPORT ENDPOINTS

@app.post("/report/wellformedness/v1", tags=["report"], responses=res_report_wellformedness_v1)
async def report_wellformedness(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_wellformedness_v1(invoice_text=invoice_text.decode("utf-8"))

@app.post("/report/schema/v1", tags=["report"], responses=res_report_schema_v1)
async def report_schema(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_schema_v1(invoice_text=invoice_text.decode("utf-8"))

@app.post("/report/syntax/v1", tags=["report"], responses=res_report_syntax_v1)
async def report_syntax(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_syntax_v1(invoice_text=invoice_text.decode("utf-8"))

@app.post("/report/peppol/v1", tags=["report"], responses=res_report_peppol_v1)
async def report_peppol(file: UploadFile = File(...)) -> Evaluation:
    invoice_text = await file.read()
    return report_peppol_v1(invoice_text=invoice_text.decode("utf-8"))

@app.get("/report/list_all/v1", tags=["report"], responses=res_report_list_all_v1)
async def report_list_all() -> ReportIDs:
    return report_list_all_v1()


@app.get("/report/list_by/v1", tags=["report"], responses=res_report_list_by_v1)
async def report_list_by(order_by: OrderBy) -> ReportIDs:
    return report_list_by_v1(order_by)

@app.get("/report/check_validity/v1", tags=["report"], responses=res_report_check_validity_v1)
async def invoice_check_validity(report_id: int) -> CheckValidReturn:
    return invoice_check_validity_v1(report_id)

@app.post("/report/lint/v1", tags=["report"], responses=res_report_lint_v1)
async def report_lint(invoice: TextInvoice) -> LintReport:
    return report_lint_v1(invoice_text=invoice.text)



# V2 ENDPOINTS

@app.post("/invoice/upload_file/v2", tags=["v2 invoice"], responses=res_invoice_upload_file_v2)
async def invoice_upload_file_v2(file: UploadFile = File(...), token = Depends(get_token)) -> ReportID:
    invoice_text = await file.read()
    return invoice_upload_file_v1(invoice_name=file.filename, invoice_text=invoice_text.decode("utf-8"), owner=Sessions.get(token=token).user) #type: ignore

@app.post("/invoice/bulk_upload_file/v2", tags=["v2 invoice"], responses=res_invoice_bulk_upload_file_v2)
async def invoice_bulk_upload_file_v2(files: List[UploadFile] = File(...), token = Depends(get_token)) -> ReportIDs:
    invoices = []
    
    for file in files:
        invoice_text = await file.read()
        invoice = TextInvoice(name=file.filename, text=invoice_text.decode("utf-8")) #type: ignore
        invoices.append(invoice)
    
    return invoice_upload_bulk_text_v1(invoices, owner=Sessions.get(token=token).user)

@app.post("/invoice/upload_text/v2", tags=["v2 invoice"], responses=res_invoice_upload_text_v2)
async def invoice_upload_text_v2(invoice: TextInvoice, token = Depends(get_token)) -> ReportID:
    return invoice_upload_text_v1(invoice_name=invoice.name, invoice_text=invoice.text, owner=Sessions.get(token=token).user)


@app.post("/invoice/bulk_upload_text/v2", tags=["v2 invoice"], responses=res_invoice_bulk_upload_text_v2)
async def invoice_upload_bulk_text_v2(invoices: List[TextInvoice], token = Depends(get_token)) -> ReportIDs:
    return invoice_upload_bulk_text_v1(invoices, owner=Sessions.get(token=token).user)

@app.post("/invoice/upload_url/v2", tags=["v2 invoice"], responses=res_invoice_upload_url_v2)
async def invoice_upload_url_v2(invoice: RemoteInvoice, token = Depends(get_token)) -> ReportID:
    return invoice_upload_url_v1(invoice_name=invoice.name, invoice_url=invoice.url, owner=Sessions.get(token=token).user)


@app.get("/export/json_report/v2", tags=["v2 export"], responses=res_export_json_report_v2)
async def export_json_report_v2(report_id: int, token = Depends(get_token)) -> Report:
    return export_json_report_v1(report_id, owner=Sessions.get(token=token).user)


@app.post("/export/bulk_json_reports/v2", tags=["v2 export"], responses=res_export_bulk_json_report_v2)
async def report_bulk_export_json_v2(report_ids: List[int], token = Depends(get_token)) -> ReportList:
    return report_bulk_export_json_v1(report_ids, owner=Sessions.get(token=token).user)


@app.get("/export/pdf_report/v2", tags=["v2 export"], responses=res_export_pdf_report_v2)
async def export_pdf_report_v2(report_id: int, token = Depends(get_token)) -> StreamingResponse:
    pdf_file = BytesIO(export_pdf_report_v1(report_id, owner=Sessions.get(token=token).user))

    # Return the PDF as a streaming response
    headers = {
        "Content-Disposition": f"attachment; filename=invoice_validation_report_{report_id}.pdf",
        "Content-Type": "application/pdf",
    }
    return StreamingResponse(pdf_file, headers=headers)

@app.post("/export/bulk_pdf_reports/v2", tags=["v2 export"], responses=res_export_bulk_pdf_report_v2)
async def report_bulk_export_pdf_v2(report_ids: List[int], token = Depends(get_token)) -> StreamingResponse:
    reports_zip = report_bulk_export_pdf_v1(report_ids, owner=Sessions.get(token=token).user)
    
    return StreamingResponse(
        reports_zip, 
        media_type="application/x-zip-compressed", 
        headers = { "Content-Disposition": f"attachment; filename=reports.zip"}
    )

@app.get("/export/html_report/v2", response_class=HTMLResponse, tags=["v2 export"], responses=res_export_html_report_v2)
async def export_html_report_v2(report_id: int, token = Depends(get_token)) -> HTMLResponse:
    html_content = export_html_report_v1(report_id, owner=Sessions.get(token=token).user)
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/report/send_email/v2", tags=["v2 report"])
async def send_email_report(email, report_id):
    pdf_file = BytesIO(export_pdf_report_v1(report_id)).read()
    send_email(pdf_file, email)
    return JSONResponse(
        status_code=200,
        content={
            "code": 200,
            "name": "Email",
            "message": "Email sent successfully"
        },
    )

@app.get("/export/csv_report/v2", tags=["v2 export"], responses=res_export_csv_report_v2)
async def export_csv_report_v2(report_id: int, token = Depends(get_token)) -> HTMLResponse:
    csv_contents = export_csv_report_v1(report_id, owner=Sessions.get(token=token).user)
    
    response = HTMLResponse(content=csv_contents, media_type='text/csv')
    response.headers['Content-Disposition'] = f'attachment; filename="invoice_validation_report_{report_id}.csv"'

    return response

@app.get("/report/list_all/v2", tags=["v2 report"], responses=res_report_list_all_v2)
async def report_list_all_v2(token = Depends(get_token)) -> ReportIDs:
    return report_list_all_v1(owner=Sessions.get(token=token).user)

@app.get("/report/list_by/v2", tags=["v2 report"], responses=res_report_list_by_v2)
async def report_list_by_v2(order_by: OrderBy, token = Depends(get_token)) -> ReportIDs:
    return report_list_by_v1(order_by, owner=Sessions.get(token=token).user)

@app.put("/report/change_name/v2", tags=["v2 report"], responses=res_report_change_name_v2)
async def report_change_name(report_id: int, new_name: str, token: str = Depends(get_token)) -> Dict:
    return report_change_name_v2(token, report_id, new_name)

@app.delete("/report/delete/v2", tags=["v2 report"], responses=res_report_delete_v2)
async def report_delete(report_id: int, token: str = Depends(get_token)) -> Dict:
    return report_delete_v2(token, report_id)

# INVOICE PROCESSING

@app.post("/invoice_processing/upload_file/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_upload_file_v2(file: UploadFile = File(...), token = Depends(get_token)) -> InvoiceID:
    invoice_text = await file.read()
    return invoice_processing_upload_text_v2(invoice_name=file.filename, invoice_text=invoice_text.decode("utf-8"), owner=Sessions.get(token=token).user) #type: ignore

@app.post("/invoice_processing/upload_text/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_upload_text_v2(invoice: TextInvoice, token = Depends(get_token)) -> InvoiceID:
    return invoice_processing_upload_text_v2(invoice_name=invoice.name, invoice_text=invoice.text, owner=Sessions.get(token=token).user)

@app.post("/invoice_processing/lint/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_lint_v2(invoice_id: int, invoice: TextInvoice = None, token = Depends(get_token)) -> LintReport:
    if not invoice:
        return invoice_processing_lint_v2(invoice_id=invoice_id, owner=Sessions.get(token=token).user)
    
    return invoice_processing_lint_v2(invoice_id=invoice_id, invoice_text=invoice.text, owner=Sessions.get(token=token).user)

@app.post("/invoice_processing/get/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_get_v2(invoice_id: int, verbose: bool = True, token = Depends(get_token)):
    return invoice_processing_get_v2(invoice_id=invoice_id, verbose=verbose, owner=Sessions.get(token=token).user)

@app.get("/invoice_processing/list_all/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_list_all_v2(is_valid: bool = None, verbose: bool = True, token = Depends(get_token)):
    return invoice_processing_list_all_v2(is_valid=is_valid, verbose=verbose, owner=Sessions.get(token=token).user)

@app.delete("/invoice_processing/delete/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_delete_v2(invoice_id: int, token = Depends(get_token)):
    return invoice_processing_delete_v2(invoice_id=invoice_id, owner=Sessions.get(token=token).user)

@app.get("/invoice_processing/query/v2", tags=["v2 invoice_processing"])
async def api_invoice_processing_query_v2(query: str, from_date: str, to_date: str, warehouse_lat: str = None, warehouse_long = None, token = Depends(get_token)):
    return invoice_processing_query_v2(query=query, from_date=from_date, to_date=to_date, warehouse_lat=warehouse_lat, warehouse_long=warehouse_long, owner=Sessions.get(token=token).user)

@app.get("/virtual_warehouse_coords")
async def get_virtual_warehouse_data(n_clusters: int, from_date: str, to_date: str, token = Depends(get_token)):
    all_data = invoice_processing_query_v2(query="heatmapCoords", from_date=from_date, to_date=to_date, owner=Sessions.get(token=token).user)
    if all_data == []:
        return {"content": {"centers": []}}

    centers = kmeans(all_data, n_clusters)
    return {"content": centers}

# AUTHENTICATION

@app.post("/auth_login/v2", tags=["v2 auth"], responses=res_auth_login_v2)
async def auth_login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = auth_login_v2(form_data.username, form_data.password).token
    user = Sessions.get(token=token).user
    return TokenAndUserReturn(access_token=token, token_type="bearer", id=user.id, name=user.name, email=user.email)

@app.post("/auth_register/v2", tags=["v2 auth"], responses=res_auth_register_v2)
async def auth_register(form_data: AuthRegister) -> AuthReturnV2:
    return auth_register_v2(form_data.name, form_data.email, form_data.password)

@app.post("/invoice/generate_hash/v2", include_in_schema=False)
async def invoice_generate_hash(invoice_text: TextInvoice) -> str:
    return invoice_generate_hash_v1(invoice_text)

@app.delete("/clear/v2", tags=["v2 auth"])
async def clear(token = Depends(get_token)):
    return clear_v2(token)





# ENDPOINTS ABOVE

if __name__ == "__main__":
    uvicorn.run(app, host=base_url, port=port)
