from datetime import datetime

from django.db import transaction
from ninja_extra import Router
from ninja_jwt.authentication import JWTAuth

from apps.common.schemas import ErrorSchema
from apps.household.models import HouseHold
from apps.household.schemas import (
    HouseHoldIn,
    HouseHoldOut,
    InviteAcceptIn,
    InviteIn,
    InviteOut,
)
from apps.users.models import CustomUser, HouseHoldRole
from apps.users.schemas import UserOut

from .services import accept_household_invite, create_invite

router = Router(tags=["HouseHold"])


@router.get("", response=list[HouseHoldOut])
def get_households(request):
    "Получение списка всех семей."
    household = HouseHold.objects.all()
    return 200, household


@router.post(
    "",
    auth=JWTAuth(),
    response={201: HouseHoldOut, 409: ErrorSchema},
)
def create_household(request, data: HouseHoldIn):
    "Создание семьи."
    with transaction.atomic():
        user = CustomUser.objects.select_for_update().get(
            pk=request.auth.pk,
        )

        if user.household_id is not None:
            return 409, {
                "code": "household_exists",
                "message": "Вы уже состоите в семье",
            }

        household = HouseHold.objects.create(
            name=data.name,
            created_at=datetime.now(),
        )

        user.household = household
        user.household_role = HouseHoldRole.OWNER
        user.save(update_fields=["household", "household_role"])

    return 201, household


@router.get(path="", auth=JWTAuth())
def get_household(request):
    """Эндпоинт требует авторизации.
    Сервер определяет пользователя по access-токену и находит его участие."""
    user = request.auth()
    return {
        "id": user.pk,
        "household": user.household,
        "household_id": user.household_id,
        "household_role": user.household_role,
    }


@router.post("invite/", auth=JWTAuth(), response={200: InviteOut, 409: ErrorSchema})
def add_household_invite(request, data: InviteIn):

    user_owner = CustomUser.objects.get(pk=request.auth.pk)
    invite = create_invite(user_owner, data.email)
    return 200, invite


@router.post("invite/accept/", auth=JWTAuth(), response={200: UserOut})
def accept_invite(request, data: InviteAcceptIn):
    accept_household_invite(user=request.user, token=data.token)
    request.user.refresh_from_db()
    return request.user
