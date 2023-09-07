from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Callable

from solana.rpc.websocket_api import connect
from solders.pubkey import Pubkey

from zeta_py import constants, pda
from zeta_py.constants import Asset
from zeta_py.pyserum.market import AsyncMarket as SerumMarket
from zeta_py.pyserum.market.orderbook import OrderBook
from zeta_py.pyserum.market.types import OrderInfo
from zeta_py.types import Side

if TYPE_CHECKING:
    from zeta_py.exchange import Exchange

import logging


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
    _serum_market: SerumMarket
    _base_zeta_vault_address: Pubkey
    _quote_zeta_vault_address: Pubkey
    _bids_subscription_task: bool = None
    _asks_subscription_task: bool = None
    _bids_last_update_slot: int = None
    _asks_last_update_slot: int = None
    _logger: logging.Logger = None

    @classmethod
    async def load(cls, asset: Asset, exchange: Exchange, subscribe: bool = False):
        # Initialize

        # Load Serum Market
        _serum_market = await SerumMarket.load(
            exchange.connection,
            exchange.pricing.account.markets[asset.to_index()],
            constants.DEX_PID[exchange.network],
        )
        bids, asks = await _serum_market.load_bids_and_asks()

        # Addresses
        _base_zeta_vault_address = pda.get_zeta_vault_address(exchange.program_id, _serum_market.state.base_mint())
        _quote_zeta_vault_address = pda.get_zeta_vault_address(exchange.program_id, _serum_market.state.quote_mint())

        logger = logging.getLogger(f"{__name__}.{cls.__name__}.{asset.name}")

        instance = cls(
            asset=asset,
            exchange=exchange,
            bids=bids,
            asks=asks,
            _serum_market=_serum_market,
            _base_zeta_vault_address=_base_zeta_vault_address,
            _quote_zeta_vault_address=_quote_zeta_vault_address,
            _logger=logger,
        )

        # Subscribe
        if subscribe:
            instance.subscribe_orderbooks()

        return instance

    @property
    def address(self) -> Pubkey:
        return self._serum_market.state.public_key()

    @property
    def oracle_address(self) -> Pubkey:
        return self.exchange.pricing.account.oracles[self.asset.to_index()]

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

    def _handle_orderbook_update(self, side: Side, data: bytes, slot: int) -> OrderBook:
        orderbook = self._serum_market._parse_bids_or_asks(data)
        if side == Side.Bid:
            self.bids = orderbook
            self._bids_last_update_slot = slot
        else:
            self.asks = orderbook
            self._asks_last_update_slot = slot
        return orderbook

    async def _subscribe_orderbook(
        self, side: Side, callback: Callable[[OrderBook], Any] = None, max_retries: int = 3
    ) -> None:
        ws_endpoint = re.sub(r"^http", "ws", self.exchange.connection._provider.endpoint_uri)
        retries = max_retries
        while True:
            async with connect(ws_endpoint) as ws:
                try:
                    await ws.account_subscribe(
                        self.address,
                        commitment=self.exchange.connection.commitment,
                        encoding="base64+zstd",
                    )
                    first_resp = await ws.recv()
                    subscription_id = first_resp[0].result
                    async for msg in ws:
                        try:
                            orderbook = self._handle_orderbook_update(
                                side, msg[0].result.value.data, msg[0].result.context.slot
                            )
                            if callback:
                                callback(orderbook)
                        except Exception as e:
                            self._logger.error(f"Error decoding account: {e}")
                    await ws.account_unsubscribe(subscription_id)
                except asyncio.CancelledError:
                    self._logger.info("WebSocket subscription task cancelled.")
                    break
                # solana_py.SubscriptionError?
                except Exception as e:
                    self._logger.error(f"Error subscribing to {self.account.__class__.__name__}: {e}")
                    retries -= 1
                    await asyncio.sleep(2)  # Pause for a while before retrying
                finally:
                    self._subscription_task = None

    def subscribe_orderbooks(self) -> None:
        # Run the subscriptions in the background
        # Subscribe bids
        if self._is_subscribed_bids:
            self._logger.warn("Already subscribed to bids")
        else:
            self._bids_subscription_task = asyncio.create_task(
                self._subscribe_orderbook(self._serum_market.state.bids(), side=Side.Bid)
            )
            self._logger.info(f"Subscribed to {self.asset.name}:bid")
        # Subscribe asks
        if self._is_subscribed_asks:
            self._logger.warn("Already subscribed to asks")
        else:
            self._asks_subscription_task = asyncio.create_task(
                self._subscribe_orderbook(self._serum_market.state.asks(), side=Side.Ask)
            )
            self._logger.info(f"Subscribed to {self.asset.name}:ask")

    async def unsubscribe_orderbooks(self) -> None:
        # Unsubscribe bids
        if not self._is_subscribed_bids:
            self._logger.warn("Already unsubscribed to bids")
        else:
            self._bids_subscription_task.cancel()
            self._bids_subscription_task = None
            self._logger.info(f"Unsubscribed to {self.asset.name}:bid")
        # Unsubscribe asks
        if not self._is_subscribed_asks:
            self._logger.warn("Already unsubscribed to asks")
        else:
            self._asks_subscription_task.cancel()
            self._asks_subscription_task = None
            self._logger.info(f"Unsubscribed to {self.asset.name}:ask")

    def print_orderbook(self, depth: int = 10, filter_tif: bool = True) -> None:
        print("Ask Orders:")
        print(*self.get_l2(Side.Ask, depth, filter_tif)[::-1], sep="\n")
        print("Bid Orders:")
        print(*self.get_l2(Side.Bid, depth, filter_tif), sep="\n")

    @staticmethod
    def _is_order_expired(
        clock_ts: int, tif_offset: int, epoch_start_ts: int, seq_num: int, epoch_start_seq_num: int
    ) -> int:
        """ """
        if tif_offset > 0:
            if epoch_start_ts + tif_offset < clock_ts or seq_num <= epoch_start_seq_num:
                return True
        return False

    def get_l2(self, side: Side, depth: int = None, filter_tif: bool = True) -> list[OrderInfo]:
        """Get the Level 2 market information."""
        orderbook = self.bids if side == Side.Bid else self.asks
        descending = orderbook._is_bids
        # The first element of the inner list is price, the second is quantity.
        levels: list[list[int]] = []
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
