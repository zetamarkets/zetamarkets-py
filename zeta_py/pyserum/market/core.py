"""Market module to interact with Serum DEX."""
from __future__ import annotations

import itertools
import logging
from typing import Optional

from zeta_py.types import Side

from . import types as t
from ._internal.queue import decode_event_queue
from .orderbook import OrderBook
from .state import MarketState

LAMPORTS_PER_SOL = 1000000000


# pylint: disable=too-many-public-methods
class MarketCore:
    """Represents a Serum Market."""

    logger = logging.getLogger("pyserum.market.Market")

    def __init__(self, market_state: MarketState) -> None:
        self.state = market_state

    def _parse_bids_or_asks(self, bytes_data: bytes) -> OrderBook:
        return OrderBook.from_bytes(self.state, bytes_data)

    @staticmethod
    def _parse_orders_for_owner(bids, asks, open_orders_account) -> Optional[list[t.Order]]:
        if not open_orders_account:
            return None

        all_orders = itertools.chain(bids.orders(), asks.orders())
        orders = [o for o in all_orders if str(o.open_order_address) == str(open_orders_account.address)]
        return orders

    def _parse_fills(self, bytes_data: bytes, limit: int) -> list[t.FilledOrder]:
        events = decode_event_queue(bytes_data, limit)
        return [
            self.parse_fill_event(event)
            for event in events
            if event.event_flags.fill and event.native_quantity_paid > 0
        ]

    def parse_fill_event(self, event: t.Event) -> t.FilledOrder:
        if event.event_flags.bid:
            side = Side.Bid
            price_before_fees = (
                event.native_quantity_released + event.native_fee_or_rebate
                if event.event_flags.maker
                else event.native_quantity_released - event.native_fee_or_rebate
            )
        else:
            side = Side.Ask
            price_before_fees = (
                event.native_quantity_released - event.native_fee_or_rebate
                if event.event_flags.maker
                else event.native_quantity_released + event.native_fee_or_rebate
            )

        price = (price_before_fees * self.state.base_spl_token_multiplier()) / (
            self.state.quote_spl_token_multiplier() * event.native_quantity_paid
        )
        size = event.native_quantity_paid / self.state.base_spl_token_multiplier()
        return t.FilledOrder(
            order_id=event.order_id,
            side=side,
            price=price,
            size=size,
            fee_cost=event.native_fee_or_rebate * (1 if event.event_flags.maker else -1),
        )
