from django.contrib.auth import authenticate, get_user_model
from ninja.errors import HttpError
from ninja_extra import Router
from ninja_jwt.tokens import RefreshToken

from .schemas import LoginIn, RegisterIn, TokenOut

User = get_user_model()
router = Router(
    tags=["auth"],
)


@router.post("register/", response=TokenOut)
def register(request, data: RegisterIn):
    user = User.objects.create_user(  # pyright: ignore[reportAttributeAccessIssue]
        email=data.email,
        password=data.password,
    )
    refresh = RefreshToken.for_user(user)  # type: ignore[misc]
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@router.post("token/", response=TokenOut)
def get_token(request, data: LoginIn):
    user = authenticate(email=data.email, password=data.password)
    if user is None:
        raise HttpError(401, "Неверный email или password")
    refresh = RefreshToken.for_user(user)  # type: ignore[misc]
    return {"access": str(refresh.access_token), "refresh": str(refresh)}
