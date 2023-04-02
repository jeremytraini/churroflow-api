# FastAPI custom exception

class InputError(Exception):
    def __init__(self, detail: str):
        self.status_code = 400
        self.detail = detail

class AuthorizationError(Exception):
    def __init__(self, detail: str):
        self.status_code = 401
        self.detail = detail

class AuthenticationError(Exception):
    def __init__(self, detail: str):
        self.status_code = 403
        self.detail = detail

class TokenError(Exception):
    def __init__(self, detail: str):
        self.status_code = 402
        self.detail = detail

class NotFoundError(Exception):
    def __init__(self, detail: str):
        self.status_code = 404
        self.detail = detail

class InternalServerError(Exception):
    def __init__(self):
        self.status_code = 500
        self.detail = 'An internal server error occured'