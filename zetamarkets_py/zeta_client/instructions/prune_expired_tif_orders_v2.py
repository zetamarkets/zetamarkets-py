from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class PruneExpiredTifOrdersV2Args(typing.TypedDict):
    limit: int


layout = borsh.CStruct("limit" / borsh.U16)


class PruneExpiredTifOrdersV2Accounts(typing.TypedDict):
    dex_program: Pubkey
    state: Pubkey
    serum_authority: Pubkey
    market: Pubkey
    bids: Pubkey
    asks: Pubkey
    event_queue: Pubkey


def prune_expired_tif_orders_v2(
    args: PruneExpiredTifOrdersV2Args,
    accounts: PruneExpiredTifOrdersV2Accounts,
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
    identifier = b"\xcc%|9\x9e\xd3\xb2\xd1"
    encoded_args = layout.build(
        {
            "limit": args["limit"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
