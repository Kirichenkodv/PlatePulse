from datetime import datetime

from ninja import Field, Schema


class HouseHoldOut(Schema):
    id: int
    name: str


class HouseHoldIn(Schema):
    name: str


class InviteIn(Schema):
    email: str


class InviteOut(Schema):
    household: int = Field(alias="household_id")
    email: str
    invite_by: int | None = Field(alias="invite_by_id")
    token_hash: str
    created_at: datetime
    expired_at: datetime | None
    revoke_at: datetime | None


class InviteAcceptIn(Schema):
    token: str
