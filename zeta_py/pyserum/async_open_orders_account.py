from __future__ import annotations

from typing import List

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solana.rpc.types import Commitment
from solders.pubkey import Pubkey

from .async_utils import load_bytes_data
from .open_orders_account import _OpenOrdersAccountCore


class AsyncOpenOrdersAccount(_OpenOrdersAccountCore):
    # Avoiding this since we get HTTP 410 Gone error on public nodes (gPA is heavily rate limited)
    # @classmethod
    # async def find_for_market_and_owner(  # pylint: disable=too-many-arguments
    #     cls,
    #     conn: AsyncClient,
    #     market: Pubkey,
    #     owner: Pubkey,
    #     program_id: Pubkey,
    #     commitment: Commitment,
    # ) -> List[AsyncOpenOrdersAccount]:
    #     args = cls._build_get_program_accounts_args(
    #         market=market, program_id=program_id, owner=owner, commitment=commitment
    #     )
    #     resp = await conn.get_program_accounts(*args)
    #     return cls._process_get_program_accounts_resp(resp)

    @classmethod
    async def load(cls, conn: AsyncClient, address: Pubkey) -> AsyncOpenOrdersAccount:
        bytes_data = await load_bytes_data(address, conn)
        return cls.from_bytes(address, bytes_data)
