"""The orders calculator module."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Optional

from django.core.exceptions import ObjectDoesNotExist
from djmoney.money import Money

if TYPE_CHECKING:
    from .models import Order
    from services.models import Price


class AbstractCalculator(ABC):
    """The abstract calculator."""

    @abstractmethod
    def calc(self, order: "Order") -> Optional[Money]:
        """Calculate the price."""


class Calculator(AbstractCalculator):
    """The calculator."""

    def calc(self, order: "Order") -> Optional[Money]:
        """Calculate the price."""
        try:
            price: "Price" = order.service.price
            if price.is_price_fixed and price.price:
                return price.price
        except ObjectDoesNotExist:
            pass
        return None
