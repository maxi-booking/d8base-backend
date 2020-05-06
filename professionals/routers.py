"""The professionals routers module."""
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, ProfessionalContactViewSet,
                    ProfessionalLocationViewSet, ProfessionalTagListViewSet,
                    ProfessionalTagViewSet, ProfessionalViewSet,
                    SubcategoryViewSet)


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r'professionals/categories', CategoryViewSet, 'categories')
    router.register(r'professionals/subcategories', SubcategoryViewSet,
                    'subcategories')
    router.register(r'professionals/tags', ProfessionalTagListViewSet,
                    'professional-tags')
    router.register(r'accounts/professionals', ProfessionalViewSet,
                    'user-professionals')
    router.register(r'accounts/professional-tags', ProfessionalTagViewSet,
                    'user-professional-tags')
    router.register(r'accounts/professional-contacts',
                    ProfessionalContactViewSet, 'user-professional-contacts')
    router.register(r'accounts/professional-locations',
                    ProfessionalLocationViewSet, 'user-professional-locations')
    return router
