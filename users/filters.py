"""The users filters module."""
from rest_framework.filters import BaseFilterBackend


class OwnerFilter(BaseFilterBackend):
    """Filter that only allows users to see their own objects."""

    def filter_queryset(self, request, queryset, view):
        """Filter the queryset."""
        if not getattr(view, 'is_owner_filter_enabled', False):
            return queryset
        field_name = getattr(view, 'owner_filter_field', 'user')
        return queryset.filter(**{
            field_name: request.user
        }).select_related(field_name)
