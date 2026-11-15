from django.db import transaction
from django.utils import timezone
from ninja.errors import HttpError

from apps.household.models import HouseHoldInvite
from apps.users.models import CustomUser, HouseHoldRole


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
