"""Market module to interact with Serum DEX."""
from __future__ import annotations

from typing import Optional, Tuple

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from zeta_py.constants import DEX_PID
from zeta_py.types import Network

# from .. import instructions
from ..async_open_orders_account import AsyncOpenOrdersAccount
from ..async_utils import load_bytes_data, load_multiple_bytes_data
from . import types as t
from ._internal.queue import decode_event_queue, decode_request_queue
from .core import MarketCore
from .orderbook import OrderBook
from .state import MarketState

LAMPORTS_PER_SOL = 1000000000


# pylint: disable=too-many-public-methods,abstract-method
class AsyncMarket(MarketCore):
    """Represents a Serum Market."""

    def __init__(
        self,
        conn: AsyncClient,
        market_state: MarketState,
    ) -> None:
        super().__init__(market_state=market_state)
        self._conn = conn

    @classmethod
    # pylint: disable=unused-argument
    async def load(
        cls,
        conn: AsyncClient,
        market_address: Pubkey,
        program_id: Pubkey = DEX_PID[Network.MAINNET],
    ) -> AsyncMarket:
        """Factory method to create a Market.

        :param conn: The connection that we use to load the data, created from `solana.rpc.api`.
        :param market_address: The market address that you want to connect to.
        :param program_id: The program id of the given market, it will use the default value if not provided.
        """
        market_state = await MarketState.async_load(conn, market_address, program_id)
        return cls(conn, market_state)

    async def load_bids(self) -> Optional[OrderBook]:
        """Load the bid order book"""
        bytes_data = await load_bytes_data(self.state.bids(), self._conn)
        if bytes_data is None:
            return None
        return self._parse_bids_or_asks(bytes_data)

    async def load_asks(self) -> Optional[OrderBook]:
        """Load the ask order book."""
        bytes_data = await load_bytes_data(self.state.asks(), self._conn)
        if bytes_data is None:
            return None
        return self._parse_bids_or_asks(bytes_data)

    async def load_bids_and_asks(self) -> Tuple[Optional[OrderBook], Optional[OrderBook]]:
        """Load the bid and ask orderbooks"""
        [bids_bytes, asks_bytes] = await load_multiple_bytes_data([self.state.bids(), self.state.asks()], self._conn)
        bids = self._parse_bids_or_asks(bids_bytes) if bids_bytes is not None else None
        asks = self._parse_bids_or_asks(asks_bytes) if asks_bytes is not None else None
        return bids, asks

    async def load_orders_for_owner(self, open_orders_account_address: Pubkey) -> Optional[list[t.Order]]:
        """Load orders for owner."""
        bids, asks = await self.load_bids_and_asks()
        open_orders_account = await AsyncOpenOrdersAccount.load(self._conn, open_orders_account_address)
        if open_orders_account is None:
            return None
        return self._parse_orders_for_owner(bids, asks, open_orders_account)

    async def load_event_queue(self) -> Optional[list[t.Event]]:
        """Load the event queue which includes the fill item and out item. For any trades two fill items are added to
        the event queue. And in case of a trade, cancel or IOC order that missed, out items are added to the event
        queue.
        """
        bytes_data = await load_bytes_data(self.state.event_queue(), self._conn)
        if bytes_data is None:
            return None
        return decode_event_queue(bytes_data)

    async def load_request_queue(self) -> Optional[list[t.Request]]:
        bytes_data = await load_bytes_data(self.state.request_queue(), self._conn)
        if bytes_data is None:
            return None
        return decode_request_queue(bytes_data)

    async def load_fills(self, limit=100) -> Optional[list[t.FilledOrder]]:
        bytes_data = await load_bytes_data(self.state.event_queue(), self._conn)
        if bytes_data is None:
            return None
        return self._parse_fills(bytes_data, limit)
