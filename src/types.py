from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union

Server_call_return = Dict[str, Any]

class Format(BaseModel):
    format: Literal["HTML", "PDF"]

class Invoice(BaseModel):
    name: str
    format: Literal["XML", "JSON", "HTML", "PDF"]
    source: Literal["url", "file_upload", "raw_data", "text"]
    data: str

class Location(BaseModel):
    type: Literal["xpath", "line"]
    xpath: Union[str, None]
    line: Union[int, None]
    column: Union[int, None]

class Violation(BaseModel):
    rule_id: str
    is_fatal: bool
    location: Location
    test: str
    message: str
    suggestion: str

class Evaluation(BaseModel):
    aspect: Literal["wellformedness", "syntax", "peppol", "schema"]
    is_valid: bool
    num_rules_fired: int
    num_rules_failed: int
    num_violations: int
    violations: List[Violation]

class Report(BaseModel):
    report_id: int
    score: int
    date_generated: str
    invoice_name: str
    invoice_raw: str
    invoice_hash: str
    is_valid: bool
    total_num_violations: int
    wellformedness:  Union[Evaluation, None]
    schemaEvaluation: Union[Evaluation, None]
    syntax: Union[Evaluation, None]
    peppol: Union[Evaluation, None]

class ReportExport(BaseModel):
    url: str
    invoice_hash: str

class QuickFixReturn(BaseModel):
    invoice: Invoice
    report: Report

class CheckValidReturn(BaseModel):
    is_valid: bool
    invoice_hash: str