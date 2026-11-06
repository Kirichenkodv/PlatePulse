from ninja import Schema


class UserIn(Schema):
    email: str
    password: str


class TokenOut(Schema):
    access: str
    refresh: str
