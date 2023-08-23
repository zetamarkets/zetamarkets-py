from __future__ import annotations

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey

from .async_utils import load_bytes_data
from .open_orders_account import _OpenOrdersAccountCore


class AsyncOpenOrdersAccount(_OpenOrdersAccountCore):
    @classmethod
    async def load(cls, conn: AsyncClient, address: Pubkey) -> AsyncOpenOrdersAccount:
        bytes_data = await load_bytes_data(address, conn)
        return cls.from_bytes(address, bytes_data)
