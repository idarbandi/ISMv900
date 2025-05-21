from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = ""
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1','0.0.0.0', '192.168.116.13', '192.168.1.101', '192.168.1.106', '192.168.1.107', '192.168.1.171']

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # local app
    "myapp.apps.MyappConfig",
    "channels",
    "invoice.apps.InvoiceConfig", # New
    "graphene_django", # Added
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

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR/ 'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "localnew.sqlite3"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

LANGUAGE_CODE = 'fa'
TIME_ZONE = 'Asia/Tehran'
DEFAULT_CHARSET = 'utf-8'
USE_I18N = True
USE_TZ = False
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ASGI_APPLICATION = "backend.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://192.168.6.165:8000",
]

CORS_ALLOW_ALL_ORIGINS = True

GRAPHENE = {
    'SCHEMA': 'filter.schema.schema',
}