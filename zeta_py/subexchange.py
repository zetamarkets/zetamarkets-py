from __future__ import annotations

import asyncio
from email import utils
from typing import Any, Callable, List
from zeta_py.assets import asset_to_index
from zeta_py.constants import Asset
from zeta_py.events import EventType
from zeta_py.market import ZetaGroupMarkets
from zeta_py.zeta_client.accounts.perp_sync_queue import PerpSyncQueue
from solders.pubkey import Pubkey
from solana.rpc.types import TxOpts


class SubExchange:
    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    @property
    def asset(self) -> Asset:
        return self._asset

    @property
    def exchange(self) -> Exchange:
        return self._exchange

    @property
    def zeta_group_address(self) -> Pubkey:
        return self._zeta_group_address

    @property
    def markets(self) -> ZetaGroupMarkets:
        return self._markets

    @property
    def perp_sync_queue(self) -> PerpSyncQueue:
        return self._perp_sync_queue

    # @property
    # def perp_sync_queue_address(self) -> Pubkey:
    #     return self._perp_sync_queue_address

    # @property
    # def halted(self) -> bool:
    #     return self.exchange.state.halt_states[asset_to_index(self.asset)].halted

    def __init__(self, asset: Asset, exchange: Exchange) -> None:
        self._asset = asset
        self._exchange = exchange

        # Load zeta group.
        underlying_mint = utils.get_underlying_mint(asset)

        # Grab zetagroupaddress manually because Pricing acc isnt loaded yet at this point
        # self._zeta_group_address = utils.get_zeta_group(
        #     self.exchange.program_id, underlying_mint
        # )[0]

        self._perp_sync_queue_address = utils.get_perp_sync_queue(
            self.exchange.program_id, self._zeta_group_address
        )[0]

        self._markets = ZetaGroupMarkets(asset, self)

    async def load(
        self,
        asset: Asset,
        opts: TxOpts,
        fetched_accs: List,
        load_from_store: bool,
        callback: Callable[[Asset, EventType, Any], Any] = None,
    ) -> None:
        """
        Loads a fresh instance of the subExchange object using on chain state.
        """
        print(f"Loading {asset.value} subExchange.")

        if self._is_loaded:
            raise "SubExchange already loaded."

        self._perp_sync_queue: PerpSyncQueue = fetched_accs[0]

        self._markets = await ZetaGroupMarkets.load(asset, opts, load_from_store)

        self.exchange.risk_calculator.update_margin_requirements(asset)

        # Set callbacks.
        self.subscribe_perp_sync_queue()

        self._is_loaded = True

        print(f"{self.asset} SubExchange loaded")
        return

    # Factory method
    @classmethod
    async def create(
        cls,
        asset: Asset,
        exchange: Exchange,
        opts: TxOpts,
        fetched_accs: List,
        load_from_store: bool,
        callback: Callable[[Asset, EventType, Any], Any] = None,
    ) -> "SubExchange":
        obj = cls(asset, exchange)
        await obj.load(asset, opts, fetched_accs, load_from_store, callback)

    # Refreshes serum markets cache
    async def update_serum_markets(self):
        print(f"Refreshing Serum markets for {self.asset.value} SubExchange.")

        await asyncio.gather(
            *[
                m.serum_market.update_decoded(self.exchange.connection)
                for m in self._markets.markets
            ],
            self._markets.perp_market.serum_market.update_decoded(
                self.exchange.connection
            ),
        )

        print(f"{self.asset.value} SubExchange Serum markets refreshed")

    def update_perp_serum_market_if_needed(self, epoch_delay: int):
        m = self._markets.perp_market

        if (
            m.serum_market.epoch_length == 0
            or m.serum_market.epoch_start_ts + m.serum_market.epoch_length + epoch_delay
            > clock_timestamp()
        ):
            return

        m.serum_market.update_decoded(self.exchange.connection)

        print(f"{self.asset.value} SubExchange perp Serum market refreshed")
