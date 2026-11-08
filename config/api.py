from ninja_extra import NinjaExtraAPI

from apps.auth.api import router as auth_router
from apps.common.exception_handlers import ExceptionHandlers
from apps.household.api import router as household_router
from apps.system.api import router as system_router
from apps.users.api import router as user_router

from .config import settings_env

api = NinjaExtraAPI(
    title=settings_env.api.TITLE,
    description=settings_env.api.DESCRIPTION,
    version=settings_env.api.VERSION,
)
ExceptionHandlers(api).register()


api.add_router("system/", system_router)
api.add_router("auth/", auth_router)
api.add_router("household/", household_router)
api.add_router("user/", user_router)
