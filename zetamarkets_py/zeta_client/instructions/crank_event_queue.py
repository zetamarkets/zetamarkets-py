from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class CrankEventQueueArgs(typing.TypedDict):
    asset: types.asset.AssetKind


layout = borsh.CStruct("asset" / types.asset.layout)


class CrankEventQueueAccounts(typing.TypedDict):
    state: Pubkey
    pricing: Pubkey
    market: Pubkey
    event_queue: Pubkey
    dex_program: Pubkey
    serum_authority: Pubkey
    perp_sync_queue: Pubkey


def crank_event_queue(
    args: CrankEventQueueArgs,
    accounts: CrankEventQueueAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["event_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["dex_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["serum_authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_sync_queue"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"C\x85a\xdf\xb2\xbc\xeb\xb5"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
