from dataclasses import dataclass
from enum import Enum
from typing import Union

from anchorpy import Event
from construct import Container
from solders.pubkey import Pubkey

from zetamarkets_py import utils
from zetamarkets_py.types import Asset, OrderCompleteType, Side


# PlaceOrderEvent but we add the args from the PlaceOrder instruction itself, as well as the tx slot and signature
@dataclass
class PlaceOrderEventWithArgs:
    # ix args
    price: float
    size: float
    side: Side

    # ix event
    fee: float
    oracle_price: float
    order_id: int
    asset: Asset
    margin_account: Pubkey
    client_order_id: int

    @classmethod
    def from_event_and_args(cls, event: Event, args: Container):
        assert event.name.startswith("PlaceOrderEvent")
        return cls(
            price=utils.convert_fixed_int_to_decimal(args.price),
            size=utils.convert_fixed_lot_to_decimal(args.size),
            side=Side.from_index(args.side.index),
            fee=utils.convert_fixed_int_to_decimal(event.data.fee),
            oracle_price=utils.convert_fixed_int_to_decimal(event.data.oracle_price),
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            margin_account=event.data.margin_account,
            client_order_id=event.data.client_order_id,
        )


# Taker trade comes from place_perp_order
# Maker trade comes from crank_event_queue and has no extra ix args
@dataclass
class TradeEventWithPlacePerpOrderArgs:
    # ix args
    price: float
    side: Side

    # ix event
    margin_account: Pubkey
    size: float
    client_order_id: int
    order_id: int
    asset: Asset
    authority: Pubkey
    is_taker: bool
    sequence_number: int
    fee: float

    @classmethod
    def from_event_and_args(cls, event: Event, args: Container):
        assert event.name.startswith("TradeEvent")
        return cls(
            price=utils.convert_fixed_int_to_decimal(args.price),
            side=Side.from_index(args.side.index),
            margin_account=event.data.margin_account,
            size=utils.convert_fixed_lot_to_decimal(event.data.size),
            client_order_id=event.data.client_order_id,
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            authority=event.data.user,
            is_taker=event.data.is_taker,
            sequence_number=event.data.sequence_number,
            fee=utils.convert_fixed_int_to_decimal(event.data.fee),
        )


@dataclass
class PlaceOrderEvent:
    fee: float
    oracle_price: float
    order_id: int
    asset: Asset
    margin_account: Pubkey
    client_order_id: int

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            fee=utils.convert_fixed_int_to_decimal(event.data.fee),
            oracle_price=utils.convert_fixed_int_to_decimal(event.data.oracle_price),
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            margin_account=event.data.margin_account,
            client_order_id=event.data.client_order_id,
        )


@dataclass
class OrderCompleteEvent:
    margin_account: Pubkey
    authority: Pubkey
    asset: Asset
    side: Side
    unfilled_size: float
    order_id: int
    client_order_id: int
    order_complete_type: OrderCompleteType

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            margin_account=event.data.margin_account,
            authority=event.data.user,
            asset=Asset.from_index(event.data.asset.index),
            side=Side.from_index(event.data.side.index),
            unfilled_size=utils.convert_fixed_lot_to_decimal(event.data.unfilled_size),
            order_id=event.data.order_id,
            client_order_id=event.data.client_order_id,
            order_complete_type=OrderCompleteType.from_index(event.data.order_complete_type.index),
        )


@dataclass
class CancelOrderEvent:
    margin_account: Pubkey
    authority: Pubkey
    asset: Asset
    side: Side
    unfilled_size: float
    order_id: int
    client_order_id: int

    @classmethod
    def from_order_complete_event(cls, event: OrderCompleteEvent):
        return cls(
            margin_account=event.margin_account,
            authority=event.authority,
            asset=event.asset,
            side=event.side,
            unfilled_size=event.unfilled_size,
            order_id=event.order_id,
            client_order_id=event.client_order_id,
        )


@dataclass
class TradeEvent:
    margin_account: Pubkey
    price: float
    size: float
    side: Side
    client_order_id: int
    order_id: int
    asset: Asset
    authority: Pubkey
    is_taker: bool
    sequence_number: int
    fee: float

    @classmethod
    def from_event(cls, event: Event):
        assert event.name.startswith(cls.__name__)
        return cls(
            margin_account=event.data.margin_account,
            price=utils.convert_fixed_int_to_decimal(event.data.cost_of_trades)
            / utils.convert_fixed_lot_to_decimal(event.data.size),
            size=utils.convert_fixed_lot_to_decimal(event.data.size),
            side=Side.Bid if event.data.is_bid else Side.Ask,
            client_order_id=event.data.client_order_id,
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            authority=event.data.user,
            is_taker=event.data.is_taker,
            sequence_number=event.data.sequence_number,
            fee=utils.convert_fixed_int_to_decimal(event.data.fee),
        )


@dataclass
class LiquidationEvent:
    liquidator_reward: float
    insurance_reward: float
    side: Side
    liquidation_price: float
    liquidation_size: float
    remaining_liquidatee_balance: float
    remaining_liquidator_balance: float
    mark_price: float
    oracle_price: float
    liquidatee: Pubkey
    liquidator: Pubkey
    asset: Asset
    liquidatee_margin_account: Pubkey
    liquidator_margin_account: Pubkey

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            liquidator_reward=utils.convert_fixed_int_to_decimal(event.data.liquidator_reward),
            insurance_reward=utils.convert_fixed_int_to_decimal(event.data.insurance_reward),
            side=Side.Bid if event.data.size > 0 else Side.Ask,
            liquidation_price=utils.convert_fixed_int_to_decimal(event.data.cost_of_trades)
            / utils.convert_fixed_lot_to_decimal(abs(event.data.size)),  # TODO: check this
            liquidation_size=utils.convert_fixed_lot_to_decimal(abs(event.data.size)),
            remaining_liquidatee_balance=utils.convert_fixed_int_to_decimal(event.data.remaining_liquidatee_balance),
            remaining_liquidator_balance=utils.convert_fixed_int_to_decimal(event.data.remaining_liquidator_balance),
            mark_price=utils.convert_fixed_int_to_decimal(event.data.mark_price),
            oracle_price=utils.convert_fixed_int_to_decimal(event.data.underlying_price),
            liquidatee=event.data.liquidatee,
            liquidator=event.data.liquidator,
            asset=Asset.from_index(event.data.asset.index),
            liquidatee_margin_account=event.data.liquidatee_margin_account,
            liquidator_margin_account=event.data.liquidator_margin_account,
        )


ZetaEvent = Union[PlaceOrderEvent, TradeEvent, CancelOrderEvent, LiquidationEvent]

ZetaEnrichedEvent = Union[PlaceOrderEventWithArgs, TradeEventWithPlacePerpOrderArgs, CancelOrderEvent, LiquidationEvent]


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
