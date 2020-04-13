"""The professionals routers module."""
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, SubcategoryViewSet


def get_router() -> SimpleRouter:
    """Return the app router."""
    router = SimpleRouter()
    router.register(r'professionals/categories', CategoryViewSet, 'categories')
    router.register(
        r'professionals/subcategories',
        SubcategoryViewSet,
        'subcategories',
    )

    return router
