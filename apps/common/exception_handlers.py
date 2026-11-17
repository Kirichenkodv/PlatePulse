from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.errors import ValidationError as NinjaValidationError

from apps.common.schemas import ErrorSchema


class ExceptionHandlers:
    def __init__(self, api: NinjaAPI) -> None:
        self.api = api

    def register(self) -> None:
        self.api.add_exception_handler(
            NinjaValidationError,
            self.handle_validation_error,
        )

    def handle_validation_error(
        self,
        request: HttpRequest,
        exc: Exception | type[Exception],
    ) -> HttpResponse:
        if not isinstance(exc, NinjaValidationError):
            raise TypeError("Ожидался экземпляр ValidationError")
        error = exc.errors[0]

        body = ErrorSchema(
            code=error["type"],
            message=error["msg"],
        )
        return self.api.create_response(
            request,
            body.model_dump(),
            status=422,
        )
