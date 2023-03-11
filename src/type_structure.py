from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union

Server_call_return = Dict[str, Any]

class OrderBy(BaseModel):
    attribute: Literal["score", "date_generated", "invoice_name", "total_num_violations"]
    is_ascending: bool

class Format(BaseModel):
    format: Literal["HTML", "PDF", "CSV"]

class Invoice(BaseModel):
    name: str
    text: str

class Location(BaseModel):
    type: Literal["xpath", "line"]
    xpath: Union[str, None] = None
    line: Union[int, None] = None
    column: Union[int, None] = None

class Violation(BaseModel):
    rule_id: str
    is_fatal: bool
    xpath: Union[str, None]
    line: Union[int, None]
    column: Union[int, None]
    test: str
    message: str
    suggestion: str

class Evaluation(BaseModel):
    aspect: Literal["wellformedness", "syntax", "peppol", "schema"]
    is_valid: bool
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

class ReportID(BaseModel):
    report_id: int

class ReportExport(BaseModel):
    url: str
    invoice_hash: str

class CheckValidReturn(BaseModel):
    is_valid: bool
    invoice_hash: str
