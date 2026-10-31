from django.db import connection
from django.db.utils import OperationalError
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(
    title="PlatePulse",
    description="Приложение для учёта, планирования меню на неделю.",
    version="0.1.0",
)


@api.get(
    "/health",
    tags=["system"],
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
        "stauts": "ok",
        "database": "ok",
    }
