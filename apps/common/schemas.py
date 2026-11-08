from ninja import Schema


class ErrorSchema(Schema):
    code: str
    message: str
