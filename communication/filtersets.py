"""The communication filtersets module."""

from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django_filters import rest_framework as filters

from .models import Review, ReviewComment


def _get_reviews(request: HttpRequest) -> QuerySet:
    """Get a list of reviews."""
    if not request:
        return Review.objects.none()
    return Review.objects.get_user_list(user=request.user)


class ReviewCommentFilterSet(filters.FilterSet):
    """The filterset class for the review comment viewset class."""

    review = filters.ModelChoiceFilter(
        label=_('review'),
        queryset=_get_reviews,
    )

    class Meta:
        """The professional list filterset class serializer META class."""

        model = ReviewComment
        fields = ('review', 'created', 'modified')
