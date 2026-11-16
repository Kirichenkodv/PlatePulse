import hashlib
import secrets
from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone
from ninja.errors import HttpError

from apps.household.models import HouseHoldInvite
from apps.users.models import CustomUser, HouseHoldRole

token = secrets.token_urlsafe(32)
token_hash = hashlib.sha256(token.encode()).hexdigest()


@transaction.atomic
def create_invite(user: CustomUser, email: str):
    if user.household_role != HouseHoldRole.OWNER:
        return 409, {
            "code": "invite_error",
            "message": "Отправитель должен быть владельцем семьи.",
        }
    if user.email == email:
        return 409, {
            "code": "email_error",
            "message": "Отправитель не может отправить приглашение самому себе.",
        }
    if user.household is None:
        raise HttpError(400, "Отправитель должен быть в семье.")
    invite = HouseHoldInvite.objects.create(
        household=user.household,
        email=email,
        invite_by=user,
        token_hash=token_hash,
        created_at=datetime.now(),
        expired_at=datetime.now() + timedelta(hours=24),
    )
    return invite


@transaction.atomic
def accept_household_invite(user: CustomUser, token: str) -> CustomUser:
    "Принятие приглашения в семью по инвайту."

    invite = (
        HouseHoldInvite.objects.select_for_update().filter(token_hash=token).first()
    )

    if invite is None:
        raise HttpError(404, "Приглашение не найдено.")
    if invite.email.casefold() != user.email.casefold():
        raise HttpError(403, "Приглашение отправлено другому пользователю.")
    if invite.revoke_at is not None:
        raise HttpError(400, "Приглашение отменено.")

    now = timezone.now()

    if invite.expired_at is not None and invite.expired_at <= now:
        raise HttpError(400, "Срок действия токена истек.")
    if invite.acceted_at is not None:
        raise HttpError(400, "Приглашение уже принято.")

    user.household = invite.household
    user.household_role = HouseHoldRole.MEMBER
    user.save(update_fields=["household", "household_role"])

    invite.acceted_at = now
    invite.save(update_fields=["acceted_at"])

    return user
