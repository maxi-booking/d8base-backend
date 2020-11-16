"""The d8b URLs module."""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView

from users.urls import get_urls as get_user_urls

from .openapi import get_openapi_urls
from .routers import get_router_urls

urlpatterns = [
    re_path(r"^$", RedirectView.as_view(pattern_name="api-root")),
    re_path(r"^admin/clearcache/", include('clearcache.urls')),
    path(settings.ADMIN_URL + "/", admin.site.urls),
    re_path(r"^adminactions/", include("adminactions.urls")),
    re_path(
        r"^api/auth/",
        include("oauth2_provider.urls", namespace="oauth2_provider"),
    ),
]
urlpatterns += i18n_patterns(
    re_path(r"^api/", include(get_router_urls())),
    re_path(r"^api/accounts/", include(get_user_urls())),
)
urlpatterns += get_openapi_urls()

if settings.DEBUG or settings.TESTS:
    import debug_toolbar

    urlpatterns += [re_path(r"^__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
