"""The d8b URLs module."""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from .openapi import get_openapi_urls
from .registration import get_registration_urls
from .routers import get_router_urls

urlpatterns = [
    path(settings.ADMIN_URL + '/', admin.site.urls),
    re_path(r'^adminactions/', include('adminactions.urls')),
]
urlpatterns += i18n_patterns(
    re_path(r'^api/', include(get_router_urls())),
    re_path('^api/accounts/', include(get_registration_urls())),
)
urlpatterns += get_openapi_urls()

if settings.DEBUG or settings.TESTS:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
