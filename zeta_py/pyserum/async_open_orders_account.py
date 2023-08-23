from __future__ import annotations

from solana.rpc.async_api import AsyncClient
from solders.instruction import Instruction
from solders.pubkey import Pubkey
from solders.system_program import CreateAccountParams, create_account

from zeta_py.pyserum._layouts.open_orders import OPEN_ORDERS_LAYOUT
from zeta_py.pyserum.instructions import DEFAULT_DEX_PROGRAM_ID

from .async_utils import load_bytes_data
from .open_orders_account import _OpenOrdersAccountCore


class AsyncOpenOrdersAccount(_OpenOrdersAccountCore):
    @classmethod
    async def load(cls, conn: AsyncClient, address: Pubkey) -> AsyncOpenOrdersAccount:
        bytes_data = await load_bytes_data(address, conn)
        return cls.from_bytes(address, bytes_data)


def make_create_open_orders_account_instruction(
    owner_address: Pubkey,
    new_account_address: Pubkey,
    lamports: int,
    program_id: Pubkey = DEFAULT_DEX_PROGRAM_ID,
) -> Instruction:
    return create_account(
        CreateAccountParams(
            from_pubkey=owner_address,
            new_account_pubkey=new_account_address,
            lamports=lamports,
            space=OPEN_ORDERS_LAYOUT.sizeof(),
            program_id=program_id,
        )
    )
