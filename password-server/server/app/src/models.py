from pydantic import BaseModel

# Auth Stuff
class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'

class TokenData(BaseModel):
    client_id: str # base64
    key: str # base64
    iv: str # base64

# End Auth Stuff

class PassInfo(BaseModel):
    name: str
    username: str
    password: str
    url: str | None

class PassFileCreationReq(BaseModel):
    client_id: str
    password: str

# Errors

class NotFoundException(Exception):
    def __init__(self, message: str = 'resource not found.'):
        super.__init__(message)