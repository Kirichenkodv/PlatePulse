from ninja import Schema

from apps.household.schemas import HouseHoldOut


class UserOut(Schema):
    id: int
    email: str
    household: HouseHoldOut | None = None
    household_role: str
