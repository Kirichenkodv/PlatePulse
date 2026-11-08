from django.contrib.auth import get_user_model
from ninja import Router

from apps.users.schemas import UserSchema

User = get_user_model()
router = Router(tags=["Users"])


@router.get(path="users/", response=list[UserSchema])
def get_users(request):
    "Получение списка всех юзеров."
    users = User.objects.all()
    return 200, users
