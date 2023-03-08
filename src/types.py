from pydantic import BaseModel
from typing import Any, Dict, Literal

Server_call_return = Dict[str, Any]
class Invoice(BaseModel):
    name: str
    format: Literal["XML", "JSON", "HTML", "PDF"]
    source: Literal["url", "file_upload", "raw_data", "text"]
    data: str

class Location(BaseModel):
    type: Literal["xpath", "line"]
    xpath: str
    line: int
    column: int

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
    violations: list[Violation]


class Report(BaseModel):
    report_id: int
    score: int
    date_generated: str
    invoice_name: str
    invoice_raw: str
    invoice_hash: str
    is_valid: bool
    total_num_violations: int
    wellformedness: Evaluation | None
    schemaEvaluation: Evaluation | None
    syntax: Evaluation | None
    peppol: Evaluation | None
