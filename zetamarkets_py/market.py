from __future__ import annotations

import asyncio
import itertools
import logging
import time
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
    This class represents a Market on Zeta.
    It wraps the matching engine interface with useful metadata and helper methods.

    Note:
        Loading the market is asynchronous, so it is recommended to use :func:`load` to
        initialize the market.
    """

    connection: AsyncClient
    """The connection to the Solana network."""
    zeta_program_id: Pubkey
    """The public key of the Zeta program."""
    matching_engine_program_id: Pubkey
    """The public key of the matching engine program."""
    asset: Asset
    """The asset being traded on the market."""

    _market_state: MarketState
    _base_zeta_vault_address: Pubkey
    _quote_zeta_vault_address: Pubkey
    _logger: logging.Logger
    _bids_subscription_task: Optional[asyncio.Task] = None
    _asks_subscription_task: Optional[asyncio.Task] = None
    _bids_last_update_slot: Optional[int] = None
    _asks_last_update_slot: Optional[int] = None

    @classmethod
    async def load(
        cls,
        network: Network,
        connection: AsyncClient,
        asset: Asset,
        market_state_address: Pubkey,
        log_level: int = logging.CRITICAL,
    ):
        """Asynchronously load the Market.

        Args:
            network (Network): The network to connect to.
            connection (AsyncClient): The connection to the Solana network.
            asset (Asset): The asset being traded on the market.
            market_state_address (Pubkey): The public key of the market state.
            log_level (int, optional): The logging level. Defaults to logging.CRITICAL.

        Raises:
            Exception: If the market state is not found at the provided address.

        Returns:
            Market: An instance of the Market class.
        """
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

        # not currently used
        logger = utils.create_logger(f"{__name__}.{cls.__name__}.{asset.name}", log_level)

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
        """Market state account address.

        Returns:
            Pubkey: The public key of the market state.
        """
        return self._market_state.own_address

    @property
    def _is_subscribed_bids(self) -> bool:
        """Property that checks if the bids are subscribed.

        Returns:
            bool: True if the bids are subscribed, False otherwise.
        """
        return self._bids_subscription_task is not None

    @property
    def _is_subscribed_asks(self) -> bool:
        """Property that checks if the asks are subscribed.

        Returns:
            bool: True if the asks are subscribed, False otherwise.
        """
        return self._asks_subscription_task is not None

    async def print_orderbook(self, depth: int = 10) -> None:
        """
        Prints the order book up to a specified depth.

        Args:
            depth (int, optional): The depth of the order book to print. Defaults to 10.
        """
        print("Ask Orders:")
        ask_l2 = await self.get_l2(Side.Ask, depth)
        if ask_l2 is not None:
            print(*ask_l2[::-1], sep="\n")
        print("Bid Orders:")
        bid_l2 = await self.get_l2(Side.Bid, depth)
        if bid_l2 is not None:
            print(*bid_l2, sep="\n")

    async def load_bids(self) -> Optional[Orderbook]:
        """
        Load the bid order book.

        Returns:
            Optional[Orderbook]: The bid order book if it exists, None otherwise.
        """
        bids = await Orderbook.load(
            self.connection, self._market_state.bids, self.connection.commitment, Side.Bid, self._market_state
        )
        return bids

    async def load_asks(self) -> Optional[Orderbook]:
        """
        Load the ask order book.

        Returns:
            Optional[Orderbook]: The ask order book if it exists, None otherwise.
        """
        asks = await Orderbook.load(
            self.connection, self._market_state.asks, self.connection.commitment, Side.Ask, self._market_state
        )
        return asks

    async def load_bids_and_asks(self) -> Tuple[Optional[Orderbook], Optional[Orderbook]]:
        """
        Load the bid and ask orderbooks.

        Returns:
            Tuple[Optional[Orderbook], Optional[Orderbook]]: A tuple containing the bid and ask orderbooks. If either
                does not exist, its value will be None.
        """
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
        """
        Load orders for a specific owner.

        Args:
            open_orders_account_address (Pubkey): The public key of the owner's open orders account.

        Returns:
            Optional[list[Order]]: A list of orders for the owner if they exist, None otherwise.
        """
        bids, asks = await self.load_bids_and_asks()
        if bids is None or asks is None:
            return None
        return self._parse_orders_for_owner(bids, asks, open_orders_account_address)

    async def load_event_queue(self) -> Optional[EventQueue]:
        """
        Load the event queue which contains matching engine events that are yet to be processed.

        Returns:
            Optional[EventQueue]: The event queue if it exists, None otherwise.
        """
        eq = await EventQueue.fetch(
            self.connection, self._market_state.event_queue, self.connection.commitment, self.matching_engine_program_id
        )
        if eq is None or not (eq.header.account_flags.initialized and eq.header.account_flags.event_queue):
            raise Exception("Invalid events queue, either not initialized or not a event queue.")
        return eq

    async def load_fills(self, limit=100) -> Optional[list[FilledOrder]]:
        """
        Load the filled orders.

        Warning: this method may not work since we've modified our event queue to only include fills.

        Args:
            limit (int, optional): The maximum number of filled orders to load. Defaults to 100.

        Returns:
            Optional[list[FilledOrder]]: A list of filled orders if they exist, None otherwise.
        """
        raise NotImplementedError

    async def get_l2(
        self, side: Side, depth: int = 1000, clock_ts: int = int(time.time())
    ) -> Optional[list[OrderInfo]]:
        """
        Get the Level 2 market information.

        Args:
            side (Side): The side of the market to get information for.
            depth (int, optional): The depth of the market to get information for. Defaults to 1000.
            clock_ts (int, optional): The timestamp of the clock. Defaults to the current time.

        Returns:
            Optional[list[OrderInfo]]: A list of order information if it exists, None otherwise.
        """
        orderbook = await (self.load_bids() if side == Side.Bid else self.load_asks())
        if orderbook is None:
            return None
        return orderbook._get_l2(depth, clock_ts)

    @staticmethod
    def _parse_orders_for_owner(
        bids: Orderbook, asks: Orderbook, open_orders_account_address: Pubkey
    ) -> Optional[list[Order]]:
        """
        Parse orders for a specific owner.

        Args:
            bids (Orderbook): The bid orderbook.
            asks (Orderbook): The ask orderbook.
            open_orders_account_address (Pubkey): The public key of the owner's open orders account.

        Returns:
            Optional[list[Order]]: A list of orders for the owner if they exist, None otherwise.
        """
        all_orders = itertools.chain(bids.orders(), asks.orders())
        orders = [o for o in all_orders if str(o.open_order_address) == str(open_orders_account_address)]
        return orders

    def _parse_fills(self, events: list[Event], limit: int) -> list[FilledOrder]:
        """
        Parse filled orders from a list of events.

        Args:
            events (list[Event]): A list of events.
            limit (int): The maximum number of filled orders to parse.

        Returns:
            list[FilledOrder]: A list of filled orders.
        """
        return [
            self._parse_fill_event(event)
            for event in events
            if event.event_flags.fill and event.native_quantity_paid > 0
        ]

    def _parse_fill_event(self, event: Event) -> FilledOrder:
        """
        Parse a fill event into a filled order.

        Args:
            event (Event): The event to parse.

        Returns:
            FilledOrder: The filled order.
        """
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
