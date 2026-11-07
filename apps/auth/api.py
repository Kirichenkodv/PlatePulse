from django.contrib.auth import authenticate, get_user_model
from jwt.exceptions import ExpiredSignatureError
from ninja.errors import HttpError
from ninja_extra import Router
from ninja_jwt.exceptions import TokenError
from ninja_jwt.tokens import RefreshToken

from .schemas import (
    ErrorOut,
    LoginIn,
    RefreshIn,
    RefreshOut,
    RegisterIn,
    TokenOut,
)

User = get_user_model()
router = Router(
    tags=["auth"],
)


@router.post(
    "register/",
    response={
        200: TokenOut,
        409: ErrorOut,
    },
)
def register(request, data: RegisterIn):
    if User.objects.filter(email=data.email).exists():
        return 409, {
            "code": "email exists",
            "message": "Пользователь с таким email существует",
        }
    user = User.objects.create_user(  # pyright: ignore[reportAttributeAccessIssue]
        email=data.email,
        password=data.password,
    )
    refresh = RefreshToken.for_user(user)  # type: ignore[misc]
    return 200, {"access": str(refresh.access_token), "refresh": str(refresh)}


@router.post("token/", response=TokenOut)
def get_token(request, data: LoginIn):
    user = authenticate(email=data.email, password=data.password)
    if user is None:
        raise HttpError(401, "Неверный email или password")
    refresh = RefreshToken.for_user(user)  # type: ignore[misc]
    return {"access": str(refresh.access_token), "refresh": str(refresh)}


@router.post(
    "refresh/",
    response={200: RefreshOut, 401: ErrorOut},
)
def refresh_token(request, data: RefreshIn):
    try:
        refresh = RefreshToken(data.refresh)
    except TokenError as exc:
        cause = exc.__cause__

        if isinstance(cause, ExpiredSignatureError):
            return 401, {
                "code": "refresh_expired",
                "message": "Срок действия refresh-токена истёк",
            }

        return 401, {
            "code": "refresh_invalid",
            "message": "Refresh-токен недействителен",
        }

    return 200, {"access": str(refresh.access_token)}
