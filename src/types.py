from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union

Server_call_return = Dict[str, Any]

class Order_By(BaseModel):
    attribute: Literal["score", "date_generated", "invoice_name", "total_num_violations"]
    is_ascending: bool

class Format(BaseModel):
    format: Literal["HTML", "PDF", "CSV"]

class Invoice(BaseModel):
    name: str
    source: Literal["url", "file_upload", "raw_data", "text"]
    data: str

class Location(BaseModel):
    type: Literal["xpath", "line"]
    xpath: Union[str, None] = None
    line: Union[int, None] = None
    column: Union[int, None] = None

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
    schema_evaluation: Union[Evaluation, None]
    syntax: Union[Evaluation, None]
    peppol: Union[Evaluation, None]

class Report_Export(BaseModel):
    url: str
    invoice_hash: str

class Quick_Fix_Return(BaseModel):
    invoice: Invoice
    report: Report

class Check_Valid_Return(BaseModel):
    is_valid: bool
    invoice_hash: str
