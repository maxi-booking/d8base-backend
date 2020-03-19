"""The users filters module."""
from rest_framework.filters import BaseFilterBackend


class OwnerFilter(BaseFilterBackend):
    """Filter that only allows users to see their own objects."""

    def filter_queryset(self, request, queryset, view):
        """Filter the queryset."""
        if getattr(view, 'is_owner_filter_enabled', False):
            return queryset.filter(user=request.user).select_related('user')
        return queryset
