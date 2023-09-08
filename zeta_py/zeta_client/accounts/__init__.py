import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class AnchorpyAccount(ABC):
    discriminator: typing.ClassVar = None
    layout: typing.ClassVar

    @classmethod
    @abstractmethod
    def decode(cls, data: bytes) -> "AnchorpyAccount":
        pass


from httpx import AsyncClient

from .cross_margin_account import CrossMarginAccount, CrossMarginAccountJSON
from .pricing import Pricing, PricingJSON
from .state import State, StateJSON
