from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union

Server_call_return = Dict[str, Any]

class OrderBy(BaseModel):
    table: Literal["date_generated", "invoice_name", "total_errors", "total_warnings"]
    is_ascending: bool

class Invoice(BaseModel):
    name: str
    source: str
    data: str

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
    test: Union[str, None]
    message: Union[str, None]
    suggestion: Union[str, None]

class Evaluation(BaseModel):
    is_valid: bool
    num_rules_failed: int
    num_warnings: int
    num_errors: int
    violations: List[Violation]

class Report(BaseModel):
    report_id: int
    date_generated: str
    invoice_name: str
    invoice_text: str
    invoice_hash: str
    is_valid: bool
    total_warnings: int
    total_errors: int
    wellformedness_evaluation:  Union[Evaluation, None]
    schema_evaluation: Union[Evaluation, None]
    syntax_evaluation: Union[Evaluation, None]
    peppol_evaluation: Union[Evaluation, None]

class ReportID(BaseModel):
    report_id: int

class ReportExport(BaseModel):
    url: str
    invoice_hash: str

class CheckValidReturn(BaseModel):
    is_valid: bool
