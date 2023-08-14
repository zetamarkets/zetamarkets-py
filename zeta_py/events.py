from enum import Enum


class EventType(Enum):
    """
    Refers to events that reflect a change in the exchange state.
    """

    EXCHANGE = 0
    """
    Expiration event for a zeta group.
    """
    EXPIRY = 1
    """
    Events that reflect a change in user state
    i.e. Margin account or orders
    """
    USER = 2
    """
    A change in the clock account.
    """
    CLOCK = 3
    """
    A trade event for the user margin account.
    """
    TRADE = 4
    """
    A trade v2 event for the user margin account.
    """
    TRADEV2 = 5
    """
    A trade v3 event for the user margin account.
    """
    TRADEV3 = 6
    """
    An OrderComplete event for the user margin account.
    Happens when an order is either fully filled or cancelled
    """
    ORDERCOMPLETE = 7
    """
    An update in the orderbook.
    """
    ORDERBOOK = 8
    """
    On oracle account change.
    """
    ORACLE = 9
    """
    On pricing account change
    """
    PRICING = 10
