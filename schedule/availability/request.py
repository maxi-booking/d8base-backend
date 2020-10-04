"""The availability request module."""

from abc import ABC, abstractmethod
from typing import Optional

import arrow
from django.conf import settings

from professionals.models import Professional
from services.models import Service

from .exceptions import AvailabilityValueError


class Request():
    """The request class."""

    professional: Professional
    service: Optional[Service] = None
    append_days: bool = False
    start_datetime: Optional[arrow.Arrow] = None
    end_datetime: Optional[arrow.Arrow] = None

    def __str__(self) -> str:
        """Return the string representation."""
        return (f"professional: {self.professional} ({self.professional.pk}), "
                f"service: {self.service}:"
                f"{self.start_datetime}-{self.end_datetime}")


class RequestValidator():
    """The request class."""

    @staticmethod
    def _validate_datetime(value: Optional[arrow.Arrow], title: str):
        """Validate the request datetime."""
        if not value or value.utcoffset().total_seconds() != 0:
            raise AvailabilityValueError(
                f"The request {title} datetime is invalid")

    def validate(self, request: Request) -> None:
        """Validate the request."""
        self._validate_datetime(request.start_datetime, "start_datetime")
        self._validate_datetime(request.end_datetime, "end_datetime")
        if request.start_datetime and request.end_datetime and \
                request.start_datetime > request.end_datetime:
            raise AvailabilityValueError(
                "The start datetime must be less than the end datetime")
        if not getattr(request, "professional", None):
            raise AvailabilityValueError("The professional is empty")
        if request.service and \
           request.professional != request.service.professional:
            raise AvailabilityValueError("The service is incorrect")


class AbstractRequestProcessor(ABC):
    """The abstract request processor."""

    _request: Request
    validator = RequestValidator()

    def _set_professional(self) -> None:
        """Set the request professional."""
        if self._request.service:
            self._request.professional = self._request.service.professional

    def _reset_date_to_midnight(self, name: str) -> None:
        """Set the dates to midnight."""
        date = getattr(self._request, name, None)
        if not date:
            return
        date = date.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        setattr(self._request, name, date)

    @abstractmethod
    def _set_dates(self) -> None:
        """Set the request dates."""

    def _set_dates_and_reset_to_midnight(self) -> None:
        """Set the request dates."""
        self._set_dates()
        self._reset_date_to_midnight("start_datetime")
        self._reset_date_to_midnight("end_datetime")

    def get(self, request: Request) -> Request:
        """Transform and prepare a request."""
        self._request = request
        self._set_dates_and_reset_to_midnight()
        self._set_professional()
        self.validator.validate(self._request)
        return self._request


class RequestAppendProcessor(AbstractRequestProcessor):
    """The request processor to append slots to the end of a year."""

    def _set_dates(self) -> None:
        """Set the request dates."""
        if not self._request.start_datetime:
            self._request.start_datetime = arrow.utcnow().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ).shift(years=1)
        if not self._request.end_datetime:
            self._request.end_datetime = arrow.utcnow().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ).shift(years=1, days=settings.AVAILABILITY_DAYS_TO_APPEND)


class RequestYearProcessor(AbstractRequestProcessor):
    """The request processor to generate slots for a year."""

    def _set_dates(self) -> None:
        """Set the request dates."""
        if not self._request.start_datetime:
            self._request.start_datetime = arrow.utcnow().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
        if not self._request.end_datetime:
            self._request.end_datetime = arrow.utcnow().replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            ).shift(years=1)
