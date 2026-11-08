from django.db import connection
from django.db.utils import DatabaseError
from ninja import Router
from ninja.schema import Schema


class HealthSchema(Schema):
    status: str
    database: str


router = Router(tags=["system"], auth=None)


@router.get(
    "",
    description="Проверяет подключение к базе данных",
    response={
        200: HealthSchema,
        503: HealthSchema,
    },
)
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return 503, {
            "status": "error",
            "database": "unavailable",
        }

    return 200, {
        "status": "ok",
        "database": "ok",
    }
