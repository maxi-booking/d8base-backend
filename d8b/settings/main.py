"""The settings module."""

# import datetime
import os

from kombu import Queue

from .env import ENV, ROOT

SITE_ROOT = ROOT()
BASE_DIR = SITE_ROOT

DATABASES = {'default': ENV.db()}

locals().update(ENV.email())
DEFAULT_FROM_EMAIL = ENV.str('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = ENV.str('SERVER_EMAIL')

ADMINS = [(x, x) for x in ENV.tuple('ADMINS')]
MANAGERS = ADMINS

SECRET_KEY = ENV.str('SECRET_KEY')
ALLOWED_HOSTS = ENV.list('ALLOWED_HOSTS')

DEBUG = ENV.bool('DEBUG')
TEMPLATE_DEBUG = ENV.bool('TEMPLATE_DEBUG')
TESTS = ENV.bool('TESTS', default=False)

AUTH_USER_MODEL = 'users.User'

# Celery
CELERY_LOGLEVEL = ENV.str('CELERY_LOGLEVEL')
BROKER_URL = ENV.str('BROKER_URL')
CELERY_RESULT_BACKEND = ENV.str('CELERY_RESULT_BACKEND')
CELERY_ALWAYS_EAGER = ENV.bool('CELERY_ALWAYS_EAGER', default=False)
CELERY_EAGER_PROPAGATES_EXCEPTIONS = ENV.bool(
    'CELERY_EAGER_PROPAGATES_EXCEPTIONS', default=False)
if ENV.str('BROKER_BACKEND', default=None):
    BROKER_BACKEND = ENV.str('BROKER_BACKEND')

# Django-cors
CORS_ORIGIN_ALLOW_ALL = ENV.bool('CORS_ORIGIN_ALLOW_ALL', default=False)
CORS_ORIGIN_REGEX_WHITELIST = []
for domain in ENV.list('CORS_ORIGIN_REGEX_WHITELIST', default=[]):
    CORS_ORIGIN_REGEX_WHITELIST.append(
        r'^(https?:\/\/)?([a-zA-Z0-9\-]+\.)?{}$'.format(domain))

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'django_filters',
    'rest_framework',
    'debug_toolbar',
    'reversion',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',

    # d8base apps
    'd8b',
    'users',
]

SITE_ID = 1

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'd8b.middleware.DisableAdminI18nMiddleware',
    'd8b.middleware.ThreadSafeUserMiddleware',
    'reversion.middleware.RevisionMiddleware',
]

ROOT_URLCONF = 'd8b.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'd8b/templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'd8b.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

INTERNAL_IPS = ['127.0.0.1']

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'd8b/static'),
    os.path.join(BASE_DIR, 'node_modules'),
)

FIXTURE_DIRS = (os.path.join(BASE_DIR, 'fixtures'), )

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), "locale"),
    os.path.join(os.path.dirname(__file__), "app_locale"),
)

EMAIL_SUBJECT_PREFIX = 'd8b: '
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/d8b.log',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'd8b': {
            'handlers': ['file', 'mail_admins'],
            'level': 'DEBUG',
        },
    }
}

# Celery
CELERY_SEND_TASK_ERROR_EMAILS = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_APP = 'd8b'
CELERY_QUEUES = (
    Queue('default'),
    Queue('priority_high'),
)
CELERY_DEFAULT_QUEUE = 'default'
CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 5

# Django restframework
REST_FRAMEWORK = {
    'DEFAULT_VERSION':
    '1.0',
    'DEFAULT_VERSIONING_CLASS':
    'rest_framework.versioning.AcceptHeaderVersioning',
    'DEFAULT_PAGINATION_CLASS':
    'nativecards.pagination.StandardPagination',
    'DEFAULT_PERMISSION_CLASSES': [
        'nativecards.permissions.DjangoModelPermissionsGet',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', )
}

# Sentry
if not DEBUG and not TESTS:  # pragma: no cover
    from sentry_sdk.integrations.django import DjangoIntegration
    import sentry_sdk
    sentry_sdk.init(
        dsn=ENV.str('SENTRY'),
        integrations=[DjangoIntegration()],
        send_default_pii=True,
    )

# Cache
CACHES = {'default': ENV.cache()}
CACHES['default']['TIMEOUT'] = 60 * 60 * 24 * 7

# DRM estensions
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 60 * 24 * 7,
    'DEFAULT_CACHE_ERRORS': False,
    'DEFAULT_USE_CACHE': 'default'
}

# Django OTP
OTP_TOTP_ISSUER = "d8base.com"

# # Simplejwt
# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': datetime.timedelta(minutes=60 * 24),
#     'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'AUTH_HEADER_TYPES': ('Bearer', 'JWT')
# }
