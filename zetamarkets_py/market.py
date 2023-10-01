from __future__ import annotations

import asyncio
import itertools
import logging
from dataclasses import dataclass
from typing import Optional, Tuple

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from zetamarkets_py import constants, pda, utils
from zetamarkets_py.constants import Asset
from zetamarkets_py.orderbook import Orderbook
from zetamarkets_py.serum_client.accounts.market_state import MarketState
from zetamarkets_py.serum_client.accounts.orderbook import OrderbookAccount
from zetamarkets_py.serum_client.accounts.queue import EventQueue
from zetamarkets_py.serum_client.types.queue import Event
from zetamarkets_py.types import FilledOrder, Network, Order, OrderInfo, Side


# Going to use ws for now, can add polling later
@dataclass
class Market:
    """
    This class represents a Perpetual Market on the Zeta platform.

    Attributes:
        connection (AsyncClient): The connection to the Solana network.
        zeta_program_id (Pubkey): The public key of the Zeta program.
        matching_engine_program_id (Pubkey): The public key of the matching engine program.
        asset (Asset): The asset being traded on this market.
        _market_state (MarketState): The state of the market.
        _base_zeta_vault_address (Pubkey): The address of the base Zeta vault.
        _quote_zeta_vault_address (Pubkey): The address of the quote Zeta vault.
        _logger (logging.Logger): The logger for this market.
        _bids_subscription_task (Optional[asyncio.Task]): The task for subscribing to bid updates.
        _asks_subscription_task (Optional[asyncio.Task]): The task for subscribing to ask updates.
        _bids_last_update_slot (Optional[int]): The slot of the last bid update.
        _asks_last_update_slot (Optional[int]): The slot of the last ask update.

    Raises:
        Exception: If the market state is not found at the provided address.
    """

    connection: AsyncClient
    zeta_program_id: Pubkey
    matching_engine_program_id: Pubkey
    asset: Asset

    _market_state: MarketState
    _base_zeta_vault_address: Pubkey
    _quote_zeta_vault_address: Pubkey
    _logger: logging.Logger
    _bids_subscription_task: Optional[asyncio.Task] = None
    _asks_subscription_task: Optional[asyncio.Task] = None
    _bids_last_update_slot: Optional[int] = None
    _asks_last_update_slot: Optional[int] = None

    @classmethod
    async def load(cls, network: Network, connection: AsyncClient, asset: Asset, market_state_address: Pubkey):
        # Initialize
        zeta_program_id = constants.ZETA_PID[network]
        matching_engine_program_id = constants.MATCHING_ENGINE_PID[network]

        # Load Market State
        _market_state = await MarketState.fetch(
            connection, market_state_address, connection.commitment, matching_engine_program_id
        )
        if _market_state is None:
            raise Exception(f"Market state not found at {market_state_address}")

        # Addresses
        _base_zeta_vault_address = pda.get_zeta_vault_address(zeta_program_id, _market_state.base_mint)
        _quote_zeta_vault_address = pda.get_zeta_vault_address(zeta_program_id, _market_state.quote_mint)

        logger = logging.getLogger(f"{__name__}.{cls.__name__}.{asset.name}")

        instance = cls(
            connection=connection,
            zeta_program_id=zeta_program_id,
            matching_engine_program_id=matching_engine_program_id,
            asset=asset,
            _market_state=_market_state,
            _base_zeta_vault_address=_base_zeta_vault_address,
            _quote_zeta_vault_address=_quote_zeta_vault_address,
            _logger=logger,
        )

        return instance

    @property
    def address(self) -> Pubkey:
        return self._market_state.own_address

    @property
    def _is_subscribed_bids(self) -> bool:
        return self._bids_subscription_task is not None

    @property
    def _is_subscribed_asks(self) -> bool:
        return self._asks_subscription_task is not None

    async def print_orderbook(self, depth: int = 10, filter_tif: bool = True) -> None:
        print("Ask Orders:")
        ask_l2 = await self.get_l2(Side.Ask, depth, filter_tif)
        if ask_l2 is not None:
            print(*ask_l2[::-1], sep="\n")
        print("Bid Orders:")
        bid_l2 = await self.get_l2(Side.Bid, depth, filter_tif)
        if bid_l2 is not None:
            print(*bid_l2, sep="\n")

    async def load_bids(self) -> Optional[Orderbook]:
        """Load the bid order book"""
        bids = await Orderbook.load(
            self.connection, self._market_state.bids, self.connection.commitment, Side.Bid, self._market_state
        )
        return bids

    async def load_asks(self) -> Optional[Orderbook]:
        """Load the ask order book."""
        asks = await Orderbook.load(
            self.connection, self._market_state.asks, self.connection.commitment, Side.Ask, self._market_state
        )
        return asks

    async def load_bids_and_asks(self) -> Tuple[Optional[Orderbook], Optional[Orderbook]]:
        """Load the bid and ask orderbooks"""
        bids_account, asks_account = await OrderbookAccount.fetch_multiple(
            self.connection,
            [self._market_state.bids, self._market_state.asks],
            self.connection.commitment,
            self.matching_engine_program_id,
        )
        bids = Orderbook(Side.Bid, bids_account, self._market_state) if bids_account else None
        asks = Orderbook(Side.Ask, asks_account, self._market_state) if asks_account else None
        return bids, asks

    async def load_orders_for_owner(self, open_orders_account_address: Pubkey) -> Optional[list[Order]]:
        """Load orders for owner."""
        bids, asks = await self.load_bids_and_asks()
        if bids is None or asks is None:
            return None
        return self._parse_orders_for_owner(bids, asks, open_orders_account_address)

    async def load_event_queue(self) -> Optional[EventQueue]:
        """Load the event queue which includes the fill item and out item. For any trades two fill items are added to
        the event queue. And in case of a trade, cancel or IOC order that missed, out items are added to the event
        queue.
        """
        eq = await EventQueue.fetch(
            self.connection, self._market_state.event_queue, self.connection.commitment, self.matching_engine_program_id
        )
        if eq is None or not (eq.header.account_flags.initialized and eq.header.account_flags.event_queue):
            raise Exception("Invalid events queue, either not initialized or not a event queue.")
        return eq

    async def load_fills(self, limit=100) -> Optional[list[FilledOrder]]:
        """Note: this method may not work since we've modified our event queue (TODO: check this))"""
        raise NotImplementedError
        # event_queue = await self.load_event_queue()
        # events = event_queue.nodes
        # return self._parse_fills(events, limit)

    async def get_l2(self, side: Side, depth: int = 1000, filter_tif: bool = True) -> Optional[list[OrderInfo]]:
        """Get the Level 2 market information."""
        orderbook = await (self.load_bids() if side == Side.Bid else self.load_asks())
        if orderbook is None:
            return None
        return orderbook._get_l2(depth, filter_tif)

    @staticmethod
    def _parse_orders_for_owner(
        bids: Orderbook, asks: Orderbook, open_orders_account_address: Pubkey
    ) -> Optional[list[Order]]:
        all_orders = itertools.chain(bids.orders(), asks.orders())
        orders = [o for o in all_orders if str(o.open_order_address) == str(open_orders_account_address)]
        return orders

    def _parse_fills(self, events: list[Event], limit: int) -> list[FilledOrder]:
        return [
            self._parse_fill_event(event)
            for event in events
            if event.event_flags.fill and event.native_quantity_paid > 0
        ]

    def _parse_fill_event(self, event: Event) -> FilledOrder:
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

        # price = (price_before_fees * self.state.base_spl_token_multiplier()) / (
        #     self.state.quote_spl_token_multiplier() * event.native_quantity_paid
        # )
        # size = event.native_quantity_paid / self.state.base_spl_token_multiplier()
        # TODO: check if this is correct
        price = utils.convert_fixed_int_to_decimal(int(price_before_fees / event.native_quantity_paid))
        size = utils.convert_fixed_lot_to_decimal(event.native_quantity_paid)
        return FilledOrder(
            order_id=event.order_id,
            side=side,
            price=price,
            size=size,
            fee_cost=event.native_fee_or_rebate * (1 if event.event_flags.maker else -1),
        )
