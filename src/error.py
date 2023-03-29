from fastapi.exceptions import HTTPException

class InputError(HTTPException):
    status_code = 400
    detail = 'The input you have provided is invalid'

class InvalidEmailError(HTTPException):
    code = 400
    detail = 'Email entered is not a valid email'

class UsedEmailError(HTTPException):
    code = 400
    detail = 'Email entered is already being used by another user'

class NonexistentEmailError(HTTPException):
    code = 400
    detail = 'Email entered does not exist'

class ShortPasswordError(HTTPException):
    code = 400
    detail = 'Length of password is less than 6 characters'

class IncorrectPasswordError(HTTPException):
    code = 400
    detail = 'Password is not correct'

class LongNameError(HTTPException):
    code = 400
    detail = 'Length of name is more than 100 characters'

class MalformedUrlError(HTTPException):
    code = 400
    detail = 'URL is malformed'

class InvalidDataUrlError(HTTPException):
    code = 400
    detail = 'URL does not point to plain text or XML data'

class FileDoesNotEndWithXmlError(HTTPException):
    code = 400
    detail = 'File does not end in .xml'

class LongFileNameError(HTTPException):
    code = 400
    detail = 'File name is longer than 100 characters'

class NoReportIdFoundError(HTTPException):
    code = 400
    detail = 'Report ID cannot be found'

class InvalidInvoiceFormatError(HTTPException):
    code = 400
    detail = 'Invoice is in an invalid format'

class NotWellformedInvoiceError(HTTPException):
    code = 400
    detail = 'Invoice is not wellformed'

class InvoiceSchemaError(HTTPException):
    code = 400
    detail = 'Invoice has schema errors'

class InvalidOrderByFormatError(HTTPException):
    code = 400
    detail = 'order_by is not in a valid format'

class NegativeReportIdError(HTTPException):
    code = 400
    detail = 'Report ID cannot be less than 0'

class LongNewNameError(HTTPException):
    code = 400
    detail = 'New name is longer than 100 characters'

class UserIsNotReportOwnerError(HTTPException):
    code = 400
    detail = 'Auth user is not the owner of the report'

class ReportFormatNotHtmlPdfError(HTTPException):
    code = 400
    detail = 'Report format is not HTML or PDF'

class AuthError(HTTPException):
    code = 401
    message = 'No message specified'

class InvalidToken(HTTPException):
    code = 402
    detail = 'Token is invalid'

class UserDidNotGenerateReportError(HTTPException):
    code = 402
    detail = 'Auth user did not generate the report'

class NotSuperuserError(HTTPException):
    code = 400
    detail = 'User is not the superuser (first user to register)'

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class AuthenticationError(HTTPException):
    status_code = 403
    detail = 'You are unauthorised to access this resource'

class NonexistentReportIdError(HTTPException):
    status_code = 404
    detail = 'Report ID does not exist'
