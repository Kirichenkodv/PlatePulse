from django.db import connection
from django.db.utils import OperationalError
from ninja_extra import NinjaExtraAPI

from .config import settings_env

api = NinjaExtraAPI(
    title=settings_env.api.TITLE,
    description=settings_env.api.DESCRIPTION,
    version=settings_env.api.VERSION,
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
    except OperationalError:
        return api.create_response(
            request,
            {"status": "error", "database": "unavailable"},
            status=503,
        )
    return {
        "status": "ok",
        "database": "ok",
    }
