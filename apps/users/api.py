from typing import TYPE_CHECKING, cast

from django.contrib.auth import get_user_model
from ninja import Router
from ninja.errors import HttpError
from ninja_jwt.authentication import JWTAuth

from apps.users.models import CustomUser
from apps.users.schemas import UserOut

if TYPE_CHECKING:
    from apps.users.models import CustomUser
User = cast("type[CustomUser]", get_user_model())
router = Router(tags=["Users"])


@router.get(
    path="users/",
    response=list[UserOut],
    auth=JWTAuth(),
    description="Получить список всех пользователей из этой семьи.",
)
def get_users(request):
    user = cast("CustomUser", request.auth)
    if user.household is None:
        raise HttpError(403, "Вы не состоите в семье.")
    users = User.objects.filter(household=user.household)
    return 200, users
