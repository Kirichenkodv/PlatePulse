import hashlib
import secrets
from datetime import datetime, timedelta

from django.db import transaction
from ninja_extra import Router
from ninja_jwt.authentication import JWTAuth

from apps.common.schemas import ErrorSchema
from apps.household.models import HouseHold, HouseHoldInvite
from apps.household.schemas import HouseHoldIn, HouseHoldOut, InviteIn, InviteOut
from apps.users.models import CustomUser, HouseHoldRole

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
    with transaction.atomic():
        user = CustomUser.objects.select_for_update().get(
            pk=request.auth.pk,
        )

        if user.household_id is not None:
            return 409, {
                "code": "household_exists",
                "message": "Вы уже состоите в семье",
            }

        household = HouseHold.objects.create(name=data.name)

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


token = secrets.token_urlsafe(32)
token_hash = hashlib.sha256(token.encode()).hexdigest()


@router.post("invite/", auth=JWTAuth(), response={200: InviteOut, 409: ErrorSchema})
def add_household_invite(request, data: InviteIn):
    with transaction.atomic():
        user_owner = CustomUser.objects.select_for_update().get(pk=request.auth.pk)
    if user_owner.household_role != HouseHoldRole.OWNER:
        return 409, {
            "code": "invite_error",
            "message": "Отправитель должен быть владельцем семьи.",
        }
    if user_owner.email == data.email:
        return 409, {
            "code": "email_error",
            "message": "Отправитель не может отправить приглашение самому себе.",
        }
    invite = HouseHoldInvite.objects.create(
        household=user_owner.household,
        email=data.email,
        invite_by=user_owner,
        token_hash=token_hash,
        created_at=datetime.now(),
        expired_at=datetime.now() + timedelta(hours=24),
        # revoke_at: datetime
    )
    return 200, invite
