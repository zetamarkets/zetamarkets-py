from __future__ import annotations
import asyncio

from dataclasses import dataclass

# https://www.attrs.org/en/stable/examples.html#defaults
from attr import define
from zeta_py import pda

from zeta_py.constants import Asset
from solana.rpc.async_api import AsyncClient

from zeta_py.program_account import ProgramAccount
from zeta_py.zeta_client.accounts.perp_sync_queue import PerpSyncQueue
from zeta_py.zeta_client.accounts.zeta_group import ZetaGroup


# Going to use ws for now, can add polling later
class Market:
    """Represents a Perp Market

    Raises:
        Exception: _description_
    """

    @dataclass
    class MarketAccounts:
        perp_sync_queue: ProgramAccount[PerpSyncQueue]
        _is_loaded = False

        async def load(self, connection: AsyncClient):
            if self._is_loaded:
                raise Exception("Market already loaded")
            await asyncio.gather(self.perp_sync_queue.load(connection))
            self._is_loaded = True

    def __init__(self, asset: Asset, exchange: Exchange):
        self.asset = asset
        self.exchange = exchange
        self.is_loaded: bool = False
        self.is_subscribed: bool = False

        underlying_mint = pda.get_underlying_mint(asset, exchange.network)
        zeta_group = ProgramAccount[ZetaGroup](
            pda.get_zeta_group(self.exchange.program.program_id, underlying_mint)[0],
            ZetaGroup,
        )
        perp_sync_queue = ProgramAccount[PerpSyncQueue](
            pda.get_perp_sync_queue(
                self.exchange.program.program_id, zeta_group.address
            )[0],
            PerpSyncQueue,
        )
        self.accounts = self.MarketAccounts(perp_sync_queue)

    async def load(self):
        # Load all accounts
        await self.accounts.load(self.exchange.connection)

        # Subscribe
        # self.accounts.perp_sync_queue.subscribe(self.exchange.network)
