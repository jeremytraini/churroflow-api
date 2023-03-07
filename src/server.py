import signal
from src.config import base_url, port
from src.health_check import health_check_v1
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


@app.post("/report/syntax/v1")
async def report_syntax(invoice: Invoice):
    return report_syntax_v1(invoice.name, invoice.format, invoice.source, invoice.data)


@app.post("/report/peppol/v1")
async def report_peppol(invoice: Invoice):
    return report_peppol_v1(invoice.name, invoice.format, invoice.source, invoice.data)


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
