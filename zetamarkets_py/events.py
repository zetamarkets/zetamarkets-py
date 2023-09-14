from dataclasses import dataclass
from enum import Enum

from solders.pubkey import Pubkey

from zetamarkets_py.zeta_client.types.asset import AssetKind
from zetamarkets_py.zeta_client.types.order_complete_type import OrderCompleteTypeKind
from zetamarkets_py.zeta_client.types.side import SideKind


class TransactionEventType(Enum):
    """
    An OrderComplete event for the user margin account.
    Happens when an order is either fully filled or cancelled
    """

    ORDERCOMPLETE = "OrderCompleteEvent"
    """
    A trade v3 event for the user margin account.
    """
    TRADE = "TradeEventV3"
    """
    A liquidation event for the user margin account.
    """
    LIQUIDATION = "LiquidationEvent"


@dataclass
class OrderCompleteEvent:
    margin_account: Pubkey
    user: Pubkey
    asset: AssetKind
    market_index: int
    side: SideKind
    unfilled_size: int
    order_id: int
    client_order_id: int
    order_complete_type: OrderCompleteTypeKind


@dataclass
class TradeEventV3:
    margin_account: Pubkey
    index: int
    size: int
    cost_of_trades: int
    is_bid: bool
    client_order_id: int
    order_id: int
    asset: AssetKind
    user: Pubkey
    is_taker: bool
    sequence_number: int
    fee: int


@dataclass
class LiquidationEvent:
    pass
