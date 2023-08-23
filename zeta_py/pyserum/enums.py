"""Serum specific enums."""

from enum import Enum


class Side(Enum):
    """Side of the orderbook to trade."""

    BID = 0
    """"""
    ASK = 1
    """"""


class OrderType(Enum):
    """Type of order."""

    LIMIT = 0
    """"""
    IOC = 1
    """"""
    POST_ONLY = 2
    """"""


class SelfTradeBehavior(Enum):
    DECREMENT_TAKE = 0
    CANCEL_PROVIDE = 1
    ABORT_TRANSACTION = 2
