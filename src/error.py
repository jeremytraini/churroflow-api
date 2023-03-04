from werkzeug.exceptions import HTTPException

class AuthenticationError(HTTPException):
    code = 403
    message = 'You are unauthorised to access this resource'

class InputError(HTTPException):
    code = 400
    message = 'The input you have provided is invalid'
