from __future__ import annotations

import asyncio
import re
from ast import List
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from solana.rpc.websocket_api import connect
from solders.pubkey import Pubkey

from zeta_py import constants, pda
from zeta_py.accounts import Account
from zeta_py.constants import Asset
from zeta_py.pyserum.enums import Side
from zeta_py.pyserum.market import AsyncMarket as SerumMarket
from zeta_py.pyserum.market.orderbook import OrderBook
from zeta_py.pyserum.market.types import OrderInfo
from zeta_py.zeta_client.accounts.perp_sync_queue import PerpSyncQueue

if TYPE_CHECKING:
    from zeta_py.exchange import Exchange


# Going to use ws for now, can add polling later
@dataclass
class Market:
    """Represents a Perp Market

    Raises:
        Exception: _description_
    """

    asset: Asset
    exchange: Exchange
    bids: OrderBook
    asks: OrderBook
    perp_sync_queue: Account[PerpSyncQueue]
    _serum_market: SerumMarket
    _bids_subscription_task: bool = None
    _asks_subscription_task: bool = None

    @classmethod
    async def create(cls, asset: Asset, exchange: Exchange, subscribe: bool = False):
        # Initialize
        asset_mint = pda.get_underlying_mint_address(asset, exchange.network)
        zeta_group_address, _ = pda.get_zeta_group_address(exchange.program.program_id, asset_mint)
        perp_sync_queue_address, _ = pda.get_perp_sync_queue_address(exchange.program.program_id, zeta_group_address)
        perp_sync_queue = await Account[PerpSyncQueue].create(
            perp_sync_queue_address, exchange.connection, PerpSyncQueue
        )

        # Load Serum Market
        _serum_market = await SerumMarket.load(
            exchange.connection,
            exchange.pricing.account.markets[asset.to_index()],
            constants.DEX_PID[exchange.network],
        )
        bids, asks = await _serum_market.load_bids_and_asks()

        instance = cls(asset, exchange, bids, asks, perp_sync_queue, _serum_market)

        # Subscribe
        if subscribe:
            instance.subscribe_orderbooks()

        return instance

    @property
    def address(self) -> Pubkey:
        return self._serum_market.state.public_key()

    @property
    def _is_subscribed_bids(self) -> bool:
        return self._bids_subscription_task is not None

    @property
    def _is_subscribed_asks(self) -> bool:
        return self._asks_subscription_task is not None

    async def _poll_orderbooks(self, interval: int = 1) -> None:
        _last_poll_ts = datetime.now()
        while True:
            if datetime.now() - _last_poll_ts > timedelta(seconds=interval):
                _last_poll_ts = datetime.now()
                self.bids, self.asks = await self._serum_market.load_bids_and_asks()
                self.print_orderbook()
            else:
                await asyncio.sleep(interval)

    def poll_orderbooks(self, interval: int = 1):
        return asyncio.create_task(self._poll_orderbooks(interval))

    async def _subscribe_orderbook(self, address: Pubkey, side: Side) -> None:
        ws_endpoint = re.sub(r"^http", "ws", self.exchange.connection._provider.endpoint_uri)
        try:
            async with connect(ws_endpoint) as ws:
                await ws.account_subscribe(
                    address,
                    commitment=self.exchange.connection.commitment,
                    encoding="base64",
                )
                first_resp = await ws.recv()
                first_resp[0].result
                while True:
                    msg = await ws.recv()
                    orderbook = self._serum_market._parse_bids_or_asks(msg[0].result.value.data)
                    if side == Side.BID:
                        self.bids = orderbook
                    else:
                        self.asks = orderbook
        finally:
            self._subscription_task = None

    def subscribe_orderbooks(self) -> None:
        # Run the subscriptions in the background
        # Subscribe bids
        if self._is_subscribed_bids:
            print("Already subscribed to bids")
        else:
            self._bids_subscription_task = asyncio.create_task(
                self._subscribe_orderbook(self._serum_market.state.bids(), side=Side.BID)
            )
            print(f"Subscribed to {self.asset.name}:bid")
        # Subscribe asks
        if self._is_subscribed_asks:
            print("Already subscribed to asks")
        else:
            self._asks_subscription_task = asyncio.create_task(
                self._subscribe_orderbook(self._serum_market.state.asks(), side=Side.ASK)
            )
            print(f"Subscribed to {self.asset.name}:ask")

    async def unsubscribe_orderbooks(self) -> None:
        # Unsubscribe bids
        if not self._is_subscribed_bids:
            print("Already unsubscribed to bids")
        else:
            self._bids_subscription_task.cancel()
            self._bids_subscription_task = None
            print(f"Unsubscribed to {self.asset.name}:bid")
        # Unsubscribe asks
        if not self._is_subscribed_asks:
            print("Already unsubscribed to asks")
        else:
            self._asks_subscription_task.cancel()
            self._asks_subscription_task = None
            print(f"Unsubscribed to {self.asset.name}:ask")

    def print_orderbook(self, depth: int = 10, filter_tif: bool = True) -> None:
        print("Ask Orders:")
        print(*self.get_l2(Side.ASK, depth, filter_tif)[::-1], sep="\n")
        print("Bid Orders:")
        print(*self.get_l2(Side.BID, depth, filter_tif), sep="\n")

    @staticmethod
    def _is_order_expired(
        clock_ts: int, tif_offset: int, epoch_start_ts: int, seq_num: int, epoch_start_seq_num: int
    ) -> int:
        """ """
        if tif_offset > 0:
            if epoch_start_ts + tif_offset < clock_ts or seq_num <= epoch_start_seq_num:
                return True
        return False

    def get_l2(self, side: Side, depth: int = None, filter_tif: bool = True) -> List[OrderInfo]:
        """Get the Level 2 market information."""
        orderbook = self.bids if side == Side.BID else self.asks
        descending = orderbook._is_bids
        # The first element of the inner list is price, the second is quantity.
        levels: List[List[int]] = []
        for node in orderbook._slab.items(descending):
            seq_num = orderbook._get_seq_num_from_slab(node.key, orderbook._is_bids)
            clock_ts = self.exchange.clock.account.unix_timestamp
            order_expired = self._is_order_expired(
                clock_ts,
                node.tif_offset,
                self._serum_market.state.epoch_start_ts(),
                seq_num,
                self._serum_market.state.start_epoch_seq_num(),
            )
            if filter_tif and order_expired:
                continue
            price = orderbook._get_price_from_slab(node)
            if len(levels) > 0 and levels[len(levels) - 1][0] == price:
                levels[len(levels) - 1][1] += node.quantity
            elif len(levels) == depth:
                break
            else:
                levels.append([price, node.quantity])
        return [
            OrderInfo(
                price=orderbook._market_state.price_lots_to_number(price_lots),
                size=orderbook._market_state.base_size_lots_to_number(size_lots),
                price_lots=price_lots,
                size_lots=size_lots,
            )
            for price_lots, size_lots in levels
        ]
