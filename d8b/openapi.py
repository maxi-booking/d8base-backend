"""The d8b OpenAPI module."""
from django.conf import settings
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def get_openapi_urls() -> list:
    """Return the OpenAPI URLs."""
    schema_view = get_schema_view(
        openapi.Info(
            title='D8base API',
            default_version=settings.REST_FRAMEWORK.get('DEFAULT_VERSION'),
            description='The d8b API documentation.',
            license=openapi.License(name='GPL-3.0 License'),
        ),
        public=True,
        permission_classes=(permissions.AllowAny, ),
    )
    return [
        re_path(
            r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0),
            name='schema-json',
        ),
        re_path(
            r'^swagger/$',
            schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui',
        ),
        re_path(
            r'^redoc/$',
            schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc',
        )
    ]
