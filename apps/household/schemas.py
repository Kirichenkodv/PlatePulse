from ninja import Schema


class HouseHoldOut(Schema):
    id: int
    name: str


class HouseHoldIn(Schema):
    name: str
