"""The d8b URLs module."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path(settings.ADMIN_URL + '/', admin.site.urls),
    re_path(r'^adminactions/', include('adminactions.urls')),
]

if settings.DEBUG or settings.TESTS:
    import debug_toolbar

    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
