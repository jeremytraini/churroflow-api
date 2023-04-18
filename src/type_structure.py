from pydantic import BaseModel
from typing import Any, Dict, List, Literal, Union

Server_call_return = Dict[str, Any]

class User(BaseModel):
    email: str
    password: str

class OrderBy(BaseModel):
    table: Literal["date_generated", "invoice_name", "total_errors", "total_warnings"]
    is_ascending: bool

class TextInvoice(BaseModel):
    name: str
    text: str
    
class RemoteInvoice(BaseModel):
    name: str
    url: str

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
    invoice_hash: str
    is_valid: bool
    total_warnings: int
    total_errors: int
    wellformedness_evaluation:  Union[Evaluation, None]
    schema_evaluation: Union[Evaluation, None]
    syntax_evaluation: Union[Evaluation, None]
    peppol_evaluation: Union[Evaluation, None]

class TokenAndUserReturn(BaseModel):
    access_token: str
    token_type: str
    id: int
    name: str
    email: str

class ReportList(BaseModel):
    reports: List[Report]

class ReportID(BaseModel):
    report_id: int
    
class InvoiceID(BaseModel):
    invoice_id: int
    
class ReportIDs(BaseModel):
    report_ids: List[int]

class ReportExport(BaseModel):
    url: str
    invoice_hash: str

class CheckValidReturn(BaseModel):
    is_valid: bool

class LintDiagnostic(BaseModel):
    rule_id: str
    line: int
    column: int
    message: str
    suggestion: Union[str, None]
    xpath: Union[str, None]
    severity: Literal["error", "warning"]

class LintReport(BaseModel):
    num_errors: int
    num_warnings: int
    report: List[LintDiagnostic]
    
class AuthRegister(BaseModel):
    name: str
    email: str
    password: str

class AuthReturnV1(BaseModel):
    auth_user_id: int

class AuthReturnV2(BaseModel):
    token: str
    id: int
