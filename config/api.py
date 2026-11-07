from django.db import connection
from django.db.utils import DatabaseError
from ninja.errors import ValidationError as NinjaValidationError
from ninja_extra import NinjaExtraAPI

from apps.auth.api import router as auth_router

from .config import settings_env

api = NinjaExtraAPI(
    title=settings_env.api.TITLE,
    description=settings_env.api.DESCRIPTION,
    version=settings_env.api.VERSION,
)


@api.exception_handler(NinjaValidationError)
def validation_error_handler(request, exc):
    error = exc.errors[0]

    return api.create_response(
        request,
        {
            "code": error["type"],
            "message": error["msg"],
        },
        status=422,
    )


@api.get(
    "/health",
    tags=["system"],
    description="Проверяет подключение к базе данных",
    auth=None,
)
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return api.create_response(
            request,
            {"status": "error", "database": "unavailable"},
            status=503,
        )
    return {
        "status": "ok",
        "database": "ok",
    }


api.add_router(
    "auth/",
    auth_router,
)
