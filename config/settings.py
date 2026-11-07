from typing import Any

from .config import settings_env

SECRET_KEY = settings_env.SECRET_KEY

DEBUG = settings_env.DEBUG

ALLOWED_HOSTS = settings_env.ALLOWED_HOSTS


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ninja_extra",
    "ninja_jwt",
    "ninja_jwt.token_blacklist",
    "apps.users",
    "apps.auth",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings_env.db.NAME,
        "USER": settings_env.db.USER,
        "PASSWORD": settings_env.db.PASSWORD,
        "HOST": settings_env.db.HOST,
        "PORT": settings_env.db.PORT,
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": ("django.contrib.auth.password_validation.MinimumLengthValidator"),
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"


MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": settings_env.redis.url,
    }
}

AUTH_USER_MODEL = "users.Customuser"

NINJA_JWT: dict[str, Any] = {
    "ACCESS_TOKEN_LIFETIME": settings_env.jwt.ACCESS_TOKEN_LIFETIME,
    "REFRESH_TOKEN_LIFETIME": settings_env.jwt.REFRESH_TOKEN_LIFETIME,
    "ALGORITHM": settings_env.jwt.ALGORITHM,
    "SIGNING_KEY": settings_env.SECRET_KEY,
    "AUTH_HEADER_TYPES": settings_env.jwt.AUTH_HEADER_TYPES,
}
