from dataclasses import dataclass
from typing import Any, Optional, Union

from anchorpy import Event
from construct import Container
from solders.pubkey import Pubkey

from zetamarkets_py import utils
from zetamarkets_py.types import Asset, OrderCompleteType, Side


# PlaceOrderEvent but we add the args from the PlaceOrder instruction itself, as well as the tx slot and signature
@dataclass
class PlaceOrderEventWithArgs:
    """Program event for placing an order.

    Note:
        This class is an extension of the :class:`PlaceOrderEvent` class. It includes additional arguments from the
        PlaceOrder instruction.
    """

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


@dataclass
class PlaceOrderEvent:
    """Program event for placing an order."""

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
    """Program event for an order being completed.

    Note: This event is emitted when an order is either fully filled, cancelled or booted (i.e. TIF expiry).
    """

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
    """Event for cancelling an order.

    Note: This event is emitted when an order is cancelled, including auto-cancels like TIF.
    """

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
    """Program event for a trade."""

    margin_account: Pubkey
    price: float
    size: float
    cost_of_trades: float
    side: Side
    client_order_id: int
    order_id: int
    asset: Asset
    authority: Pubkey
    is_taker: bool
    sequence_number: int
    fee: float
    pnl: float

    @classmethod
    def from_event(cls, event: Event):
        assert event.name.startswith(cls.__name__)
        return cls(
            margin_account=event.data.margin_account,
            price=utils.convert_fixed_int_to_decimal(event.data.price),
            size=utils.convert_fixed_lot_to_decimal(event.data.size),
            cost_of_trades=utils.convert_fixed_int_to_decimal(event.data.cost_of_trades),
            side=Side.Bid if event.data.is_bid else Side.Ask,
            client_order_id=event.data.client_order_id,
            order_id=event.data.order_id,
            asset=Asset.from_index(event.data.asset.index),
            authority=event.data.user,
            is_taker=event.data.is_taker,
            sequence_number=event.data.sequence_number,
            fee=utils.convert_fixed_int_to_decimal(event.data.fee),
            pnl=utils.convert_fixed_int_to_decimal(event.data.pnl),
        )


@dataclass
class LiquidationEvent:
    """Program event for a liquidation."""

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


@dataclass
class ApplyFundingEvent:
    """Program event for funding being applied to a position."""

    margin_account: Pubkey
    authority: Pubkey
    asset: Asset
    balance_change: float
    remaining_balance: float
    funding_rate: float
    oracle_price: float
    position_size: float

    @classmethod
    def from_event(cls, event: Event):
        assert event.name == cls.__name__
        return cls(
            margin_account=event.data.margin_account,
            authority=event.data.user,
            asset=Asset.from_index(event.data.asset.index),
            balance_change=utils.convert_fixed_int_to_decimal(event.data.balance_change),
            remaining_balance=utils.convert_fixed_int_to_decimal(event.data.remaining_balance),
            funding_rate=utils.convert_fixed_int_to_decimal(event.data.funding_rate),
            oracle_price=utils.convert_fixed_int_to_decimal(event.data.oracle_price),
            position_size=utils.convert_fixed_lot_to_decimal(event.data.position_size),
        )


ZetaEvent = Union[PlaceOrderEvent, TradeEvent, CancelOrderEvent, LiquidationEvent, ApplyFundingEvent]

ZetaEnrichedEvent = Union[PlaceOrderEventWithArgs, TradeEvent, CancelOrderEvent, LiquidationEvent, ApplyFundingEvent]


@dataclass
class EventMeta:
    slot: int
    error: Optional[Any]

    @property
    def is_successful(self) -> bool:
        return self.error is None
