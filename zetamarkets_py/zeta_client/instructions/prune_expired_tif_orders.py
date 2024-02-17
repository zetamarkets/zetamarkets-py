from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class PruneExpiredTifOrdersAccounts(typing.TypedDict):
    dex_program: Pubkey
    state: Pubkey
    serum_authority: Pubkey
    market: Pubkey
    bids: Pubkey
    asks: Pubkey
    event_queue: Pubkey


def prune_expired_tif_orders(
    accounts: PruneExpiredTifOrdersAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x18\xe3\xe2\xd4]\x1a\xf2\xe6"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
