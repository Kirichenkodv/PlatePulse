from ninja import Schema


class RegisterIn(Schema):
    email: str
    password: str


class TokenOut(Schema):
    access: str
    refresh: str
