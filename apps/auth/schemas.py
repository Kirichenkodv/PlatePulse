from ninja import Schema


class RegisterIn(Schema):
    email: str
    password: str


class TokenOut(Schema):
    access: str
    refresh: str


class LoginIn(Schema):
    email: str
    password: str


class RefreshIn(Schema):
    refresh: str


class RefreshOut(Schema):
    access: str


class ErrorOut(Schema):
    code: str
    message: str
