from ninja import Schema

from apps.household.schemas import HouseHoldOut


class UserSchema(Schema):
    email: str
    household: HouseHoldOut | None = None
    household_role: str
