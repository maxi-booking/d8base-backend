"""The users routers module."""
from rest_framework.routers import SimpleRouter

from .views import (UserContactViewSet, UserLanguageViewSet,
                    UserLocationViewSet, UserSavedProfessionalViewSet,
                    UserSettingsViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r'accounts/settings', UserSettingsViewSet, 'user-settings')
    router.register(r'accounts/languages', UserLanguageViewSet,
                    'user-languages')
    router.register(r'accounts/saved-professionals',
                    UserSavedProfessionalViewSet, 'user-saved-professionals')
    router.register(r'accounts/locations', UserLocationViewSet,
                    'user-locations')
    router.register(r'accounts/contacts', UserContactViewSet, 'user-contacts')

    return router
