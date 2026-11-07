from typing import Any

from ninja import Schema
from pydantic import (
    EmailStr,
    Field,
    ValidationError,
    ValidatorFunctionWrapHandler,
    field_validator,
)
from pydantic_core import PydanticCustomError


class RegisterIn(Schema):
    email: EmailStr = Field(
        ...,
        min_length=1,
        max_length=254,
    )
    password: str = Field(
        ...,
        min_length=1,
        max_length=254,
    )

    @field_validator("email", mode="wrap")
    @classmethod
    def validate_email(
        cls,
        value: Any,
        handler: ValidatorFunctionWrapHandler,
    ) -> str:
        if isinstance(value, str) and not value.strip():
            raise PydanticCustomError(
                "email_empty",
                "Email не должен быть пустым",
            )

        try:
            return handler(value)
        except ValidationError as exc:
            raise PydanticCustomError(
                "email_invalid",
                "Укажите корректный email",
            ) from exc


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
