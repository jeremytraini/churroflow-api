from fastapi.exceptions import HTTPException

class InputError(HTTPException):
    status_code = 400
    detail = 'The input you have provided is invalid'

class InvalidEmailError(HTTPException):
    code = 400
    message = 'Email entered is not a valid email'

class UsedEmailError(HTTPException):
    code = 400
    message = 'Email entered is already being used by another user'

class NonexistentEmailError(HTTPException):
    code = 400
    message = 'Email entered does not exist'

class ShortPasswordError(HTTPException):
    code = 400
    message = 'Length of password is less than 6 characters'

class IncorrectPasswordError(HTTPException):
    code = 400
    message = 'Password is not correct'

class LongNameError(HTTPException):
    code = 400
    message = 'Length of name is more than 100 characters'

class MalformedUrlError(HTTPException):
    code = 400
    message = 'URL is malformed'

class InvalidDataUrlError(HTTPException):
    code = 400
    message = 'URL does not point to plain text or XML data'

class FileDoesNotEndWithXmlError(HTTPException):
    code = 400
    message = 'File does not end in .xml'

class LongFileNameError(HTTPException):
    code = 400
    message = 'File name is longer than 100 characters'

class NoReportIdFoundError(HTTPException):
    code = 400
    message = 'Report ID cannot be found'

class InvalidInvoiceFormatError(HTTPException):
    code = 400
    message = 'Invoice is in an invalid format'

class NotWellformedInvoiceError(HTTPException):
    code = 400
    message = 'Invoice is not wellformed'

class InvoiceSchemaError(HTTPException):
    code = 400
    message = 'Invoice has schema errors'

class InvalidOrderByFormatError(HTTPException):
    code = 400
    message = 'order_by is not in a valid format'

class NegativeReportIdError(HTTPException):
    code = 400
    message = 'Report ID cannot be less than 0'

class LongNewNameError(HTTPException):
    code = 400
    message = 'New name is longer than 100 characters'

class UserIsNotReportOwnerError(HTTPException):
    code = 400
    message = 'Auth user is not the owner of the report'

class ReportFormatNotHtmlPdfError(HTTPException):
    code = 400
    message = 'Report format is not HTML or PDF'

class AuthError(HTTPException):
    code = 401
    message = 'No message specified'

class InvalidToken(HTTPException):
    code = 402
    message = 'Token is invalid'

class UserDidNotGenerateReportError(HTTPException):
    code = 402
    message = 'Auth user did not generate the report'

class NotSuperuserError(HTTPException):
    code = 400
    message = 'User is not the superuser (first user to register)'

class AccessError(HTTPException):
    code = 403
    message = 'No message specified'

class AuthenticationError(HTTPException):
    status_code = 403
    detail = 'You are unauthorised to access this resource'

class NonexistentReportIdError(HTTPException):
    status_code = 404
    detail = 'Report ID does not exist'
