"""The settings module."""

# import datetime
import os

from corsheaders.defaults import default_headers
from kombu import Queue

from .env import ROOT, get_env

ENV = get_env()
SITE_ROOT = ROOT()
BASE_DIR = SITE_ROOT

DATABASES = {"default": ENV.db()}

locals().update(ENV.email())
DEFAULT_FROM_EMAIL = ENV.str("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = ENV.str("SERVER_EMAIL")

ADMINS = [(x, x) for x in ENV.tuple("ADMINS")]
MANAGERS = ADMINS

SECRET_KEY = ENV.str("SECRET_KEY")
ALLOWED_HOSTS = ENV.list("ALLOWED_HOSTS")

DEBUG = ENV.bool("DEBUG")
TEMPLATE_DEBUG = ENV.bool("TEMPLATE_DEBUG")
TESTS = ENV.bool("TESTS", default=False)

AUTH_USER_MODEL = "users.User"
USER_TIME_ZONE_HEADER = "x-timezone"

# Django-cors
CORS_ORIGIN_ALLOW_ALL = ENV.bool("CORS_ORIGIN_ALLOW_ALL", default=False)
CORS_ORIGIN_REGEX_WHITELIST = []
for domain in ENV.list("CORS_ORIGIN_REGEX_WHITELIST", default=[]):
    CORS_ORIGIN_REGEX_WHITELIST.append(
        r"^(https?:\/\/)?([a-zA-Z0-9\-]+\.)?{}$".format(domain))

CORS_ALLOW_HEADERS = list(default_headers) + [
    USER_TIME_ZONE_HEADER.lower(),
]

# Application definition
INSTALLED_APPS = [
    "corsheaders",
    "modeltranslation",
    "clearcache",
    "django.contrib.postgres",
    "django.contrib.admin",
    "django.contrib.humanize",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.gis",
    "django_extensions",
    "django_filters",
    "oauth2_provider",
    "rest_framework",
    "rest_framework_gis",
    "rest_registration",
    "debug_toolbar",
    "reversion",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_hotp",
    "django_otp.plugins.otp_static",
    "phonenumber_field",
    "adminactions",
    "cities",
    "drf_yasg",
    "crispy_forms",
    "admin_auto_filters",
    "imagekit",
    "adminsortable",
    "djmoney",
    "djmoney.contrib.exchange",
    "push_notifications",
    "django_elasticsearch_dsl",

    # d8base apps
    "d8b",
    "users",
    "location",
    "contacts",
    "professionals",
    "communication",
    "services",
    "schedule",
    "orders",
    "search",
]

SITE_ID = 1

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "d8b.middleware.DisableAdminI18nMiddleware",
    "d8b.middleware.ThreadSafeUserMiddleware",
    "users.middleware.UserTimezoneMiddleware",
    "reversion.middleware.RevisionMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "oauth2_provider.backends.OAuth2Backend",
    "django.contrib.auth.backends.ModelBackend"
]

if not DEBUG:  # pragma: no cover
    SECURE_BROWSER_XSS_FILTER = True

    SESSION_COOKIE_SAMESITE = "Strict"
    SESSION_COOKIE_SECURE = "Secure"
    SESSION_COOKIE_HTTPONLY = True

    CSRF_COOKIE_HTTPONLY = False
    CSRF_COOKIE_SAMESITE = "Strict"

    CSRF_COOKIE_SECURE = "Secure"

ROOT_URLCONF = "d8b.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "d8b/templates"), ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.static",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "d8b.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": ("django.contrib.auth.password_validation."
                 "UserAttributeSimilarityValidator"),
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

TIME_ZONE = "UTC"

USE_TZ = True

STATIC_URL = "/static/"

MEDIA_URL = "/media/"

INTERNAL_IPS = ["127.0.0.1"]

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "d8b/static"),
    os.path.join(BASE_DIR, "node_modules"),
)

FIXTURE_DIRS = (os.path.join(BASE_DIR, "fixtures"), )

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), "locale"),
    os.path.join(os.path.dirname(__file__), "app_locale"),
)

DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Logs
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    # "root": {
    #     "level": "WARNING",
    #     "handlers": ["file", "mail_admins"]
    # },
    "formatters": {
        "verbose": {
            "format": ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            "datefmt": "%d/%b/%Y %H:%M:%S"
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        }
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "logs/d8b.log",
            "formatter": "verbose"
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "formatter": "verbose"
        },
    },
    "loggers": {
        "d8b": {
            "handlers": ["file", "mail_admins"],
            "level": "DEBUG",
        },
    }
}

# Celery
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_APP = "d8b"
CELERY_QUEUES = (
    Queue("default"),
    Queue("priority_high"),
)
CELERY_DEFAULT_QUEUE = "default"
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 5

# Django restframework
REST_FRAMEWORK = {
    "DEFAULT_VERSION":
        "1.0",
    "DEFAULT_VERSIONING_CLASS":
        "rest_framework.versioning.AcceptHeaderVersioning",
    "DEFAULT_PAGINATION_CLASS":
        "d8b.pagination.StandardPagination",
    "PAGE_SIZE":
        100,
    "HTML_SELECT_CUTOFF":
        100,
    "DEFAULT_PERMISSION_CLASSES": [
        "d8b.permissions.DjangoModelPermissionsGet",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES":
        ["rest_framework.renderers.JSONRenderer"] if not DEBUG else [
            "rest_framework.renderers.BrowsableAPIRenderer",
            "rest_framework.renderers.JSONRenderer",
        ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
        "users.filters.OwnerFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.SessionAuthentication",
    )
}

# sentry
if not DEBUG and not TESTS:  # pragma: no cover
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=ENV.str("SENTRY"),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

# Cache
CACHES = {"default": ENV.cache()}
CACHES["default"]["TIMEOUT"] = 60 * 60 * 24 * 7

# DRM estensions
REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_CACHE_RESPONSE_TIMEOUT": 60 * 60 * 24 * 7,
    "DEFAULT_CACHE_ERRORS": False,
    "DEFAULT_USE_CACHE": "default"
}

# Django OTP
OTP_TOTP_ISSUER = "d8base.com"

# Django cities
CITIES_FILES = {
    "city": {
        "filename": ENV.str("CITIES_FILES", default="allCountries.zip"),
        "urls": ["http://download.geonames.org/export/dump/" + "{filename}"]
    },
}
CITIES_POSTAL_CODES = ENV.list("CITIES_POSTAL_CODES", default=["ALL"])
CITIES_PLUGINS = [
    "cities.plugin.postal_code_ca.Plugin",
    "cities.plugin.reset_queries.Plugin",
]

# Django phonenumber
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"

# Django rest registration
USER_FIELDS = [
    "id", "email", "first_name", "last_name", "patronymic", "phone", "gender",
    "birthday", "nationality", "account_type", "languages", "locations",
    "contacts", "is_confirmed", "avatar"
]
USER_READONLY_FIELDS = ["languages", "locations", "contacts", "is_confirmed"]
USER_EDITABLE_FIELDS = [
    f for f in USER_FIELDS if f not in USER_READONLY_FIELDS
]
REST_REGISTRATION = {
    "USER_VERIFICATION_FLAG_FIELD":
        "is_confirmed",
    "REGISTER_VERIFICATION_ENABLED":
        True,
    "REGISTER_VERIFICATION_URL":
        ENV.str("REGISTER_VERIFICATION_URL"),
    "REGISTER_EMAIL_VERIFICATION_ENABLED":
        True,
    "REGISTER_EMAIL_VERIFICATION_URL":
        ENV.str("REGISTER_EMAIL_VERIFICATION_URL"),
    "RESET_PASSWORD_VERIFICATION_ENABLED":
        True,
    "RESET_PASSWORD_VERIFICATION_URL":
        ENV.str("RESET_PASSWORD_VERIFICATION_URL"),
    "PROFILE_SERIALIZER_CLASS":
        "users.serializers.ProfileSerializer",
    "REGISTER_OUTPUT_SERIALIZER_CLASS":
        "users.serializers.RegisterTokenSerializer",
    "USER_PUBLIC_FIELDS":
        USER_FIELDS,
    "USER_EDITABLE_FIELDS":
        USER_EDITABLE_FIELDS,
    "VERIFICATION_FROM_EMAIL":
        DEFAULT_FROM_EMAIL,
}

# Django OAuth toolkit
JWT_APPLICATION_NAME = "JWT"
OAUTH2_PROVIDER = {
    "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
    "ACCESS_TOKEN_EXPIRE_SECONDS": 60 * 60 * 24 * 7,
    "SCOPES": {
        "read": "Read scope",
        "write": "Write scope",
        "groups": "Access to your groups"
    }
}

# Swagger
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header"
        }
    }
}

# Django money
DEFAULT_CURRENCY = "USD"
BASE_CURRENCY = DEFAULT_CURRENCY
CURRENCIES = ("RUB", "EUR", "CAD", "USD")
EXCHANGE_BACKEND = "djmoney.contrib.exchange.backends.FixerBackend"
FIXER_ACCESS_KEY = ENV.str("FIXER_ACCESS_KEY")

# Push notifications
PUSH_NOTIFICATIONS_SETTINGS = {
    "FCM_API_KEY": ENV.str("FCM_API_KEY"),
    "UPDATE_ON_DUPLICATE_REG_ID": True,
    "UNIQUE_REG_ID": True,
}

# Elasticsearch
ELASTICSEARCH_DSL = {
    "default": {
        "hosts": ENV.str("ELASTICSEARCH_URL")
    },
}
ELASTICSEARCH_DSL_PARALLEL = True
