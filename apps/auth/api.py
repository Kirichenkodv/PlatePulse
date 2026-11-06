from django.contrib.auth import get_user_model
from ninja_extra import Router
from ninja_jwt.tokens import RefreshToken

from .schemas import TokenOut, UserIn

User = get_user_model()
router = Router(
    tags=["auth"],
)

# @router.get("/", tags=['auth'])
# def Hello(request):
#     return {"message": "hello"}


@router.post("register/", response=TokenOut)
def register(request, data: UserIn):
    user = User.objects.create_user(  # pyright: ignore[reportAttributeAccessIssue]
        email=data.email,
        password=data.password,
    )
    refresh = RefreshToken.for_user(user)  # type: ignore[misc]
    return {"access": str(refresh.access_token), "refresh": str(refresh)}
