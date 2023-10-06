from dataclasses import dataclass
from enum import Enum
from typing import Union

from anchorpy import Event
from construct import Container
from solders.pubkey import Pubkey

from zetamarkets_py.types import Asset, OrderCompleteType, Side

# PlaceOrderEvent but we add the args from the PlaceOrder instruction itself, as well as the tx slot and signature
@dataclass
class PlaceOrderEventWithArgs:
    # ix args
    price: int
    size: int
    side: Side

    # ix event
    fee: int
    oracle_price: int
    order_id: int
    expiry_ts: int
    asset: Asset
    margin_account: Pubkey
    client_order_id: int

    @classmethod
    def from_event_and_args(cls, event: Event, args: Container):
        assert event.name.startswith("PlaceOrderEvent")
        return cls(
            price=args.price,
            size=args.size,
            side=args.side,
            fee=event.data.fee,
            oracle_price=event.data.oracle_price,
            order_id=event.data.order_id,
            expiry_ts=event.data.expiry_ts,
            asset=Asset.from_index(event.data.asset.index),
            margin_account=event.data.margin_account,
            client_order_id=event.data.client_order_id,
        )
    
# Taker trade comes from place_perp_order
# Maker trade comes from crank_event_queue and has no extra ix args
@dataclass
class TradeEventWithPlacePerpOrderArgs:
    # ix args
    price: int
    side: Side
    
    # ix event
    margin_account: Pubkey
    index: int
    size: int
    cost_of_trades: int
    is_bid: bool
    client_order_id: int
    order_id: int
    asset: Asset
    user: Pubkey
    is_taker: bool
    sequence_number: int
    fee: int

    @classmethod
    def from_event_and_args(cls, event: Event, args: Container):
        assert event.name.startswith("TradeEvent")
        return cls(
            price=args.price,
            side=args.side,
            margin_account=event.data.margin_account,
            index=event.data.index,
            size=event.data.size,
            cost_of_trades=event.data.cost_of_trades,
            is_bid=event.data.is_bid,
            client_order_id=event.data.client_order_id,
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            user=event.data.user,
            is_taker=event.data.is_taker,
            sequence_number=event.data.sequence_number,
            fee=event.data.fee,
        )



@dataclass
class PlaceOrderEvent:
    fee: int
    oracle_price: int
    order_id: int
    expiry_ts: int
    asset: Asset
    margin_account: Pubkey
    client_order_id: int

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            fee=event.data.fee,
            oracle_price=event.data.oracle_price,
            order_id=event.data.order_id,
            expiry_ts=event.data.expiry_ts,
            asset=Asset.from_index(event.data.asset.index),
            margin_account=event.data.margin_account,
            client_order_id=event.data.client_order_id,
        )


@dataclass
class OrderCompleteEvent:
    margin_account: Pubkey
    user: Pubkey
    asset: Asset
    market_index: int
    side: Side
    unfilled_size: int
    order_id: int
    client_order_id: int
    order_complete_type: OrderCompleteType

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            margin_account=event.data.margin_account,
            user=event.data.user,
            asset=Asset.from_index(event.data.asset.index),
            market_index=event.data.market_index,
            side=Side.from_index(event.data.side.index),
            unfilled_size=event.data.unfilled_size,
            order_id=event.data.order_id,
            client_order_id=event.data.client_order_id,
            order_complete_type=OrderCompleteType.from_index(event.data.order_complete_type.index),
        )


@dataclass
class TradeEvent:
    margin_account: Pubkey
    index: int
    size: int
    cost_of_trades: int
    is_bid: bool
    client_order_id: int
    order_id: int
    asset: Asset
    user: Pubkey
    is_taker: bool
    sequence_number: int
    fee: int

    @classmethod
    def from_event(cls, event: Event):
        assert event.name.startswith(cls.__name__)
        return cls(
            margin_account=event.data.margin_account,
            index=event.data.index,
            size=event.data.size,
            cost_of_trades=event.data.cost_of_trades,
            is_bid=event.data.is_bid,
            client_order_id=event.data.client_order_id,
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            user=event.data.user,
            is_taker=event.data.is_taker,
            sequence_number=event.data.sequence_number,
            fee=event.data.fee,
        )


@dataclass
class LiquidationEvent:
    liquidator_reward: int
    insurance_reward: int
    cost_of_trades: int
    size: int
    remaining_liquidatee_balance: int
    remaining_liquidator_balance: int
    mark_price: int
    underlying_price: int
    liquidatee: Pubkey
    liquidator: Pubkey
    asset: Asset
    liquidatee_margin_account: Pubkey
    liquidator_margin_account: Pubkey

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            liquidator_reward=event.data.liquidator_reward,
            insurance_reward=event.data.insurance_reward,
            cost_of_trades=event.data.cost_of_trades,
            size=event.data.size,
            remaining_liquidatee_balance=event.data.remaining_liquidatee_balance,
            remaining_liquidator_balance=event.data.remaining_liquidator_balance,
            mark_price=event.data.mark_price,
            underlying_price=event.data.underlying_price,
            liquidatee=event.data.liquidatee,
            liquidator=event.data.liquidator,
            asset=Asset.from_index(event.data.asset.index),
            liquidatee_margin_account=event.data.liquidatee_margin_account,
            liquidator_margin_account=event.data.liquidator_margin_account,
        )

EventSubscribeResponse = Union[
    PlaceOrderEvent,
    TradeEvent,
    OrderCompleteEvent,
    LiquidationEvent
]

TransactionSubscribeResponse = Union[
    PlaceOrderEventWithArgs,
    TradeEventWithPlacePerpOrderArgs,
    OrderCompleteEvent,
    TradeEvent,
    LiquidationEvent
]

class TransactionEvent(Enum):
    """
    A place order event for the user margin account.
    """

    PlaceOrderEvent = PlaceOrderEvent
    """
    An OrderComplete event for the user margin account.
    Happens when an order is either fully filled or cancelled
    """

    OrderCompleteEvent = OrderCompleteEvent
    """
    A trade event for the user margin account.
    """
    TradeEvent = TradeEvent
    """
    A liquidation event for the user margin account.
    """
    LiquidationEvent = LiquidationEvent
