from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from .. import types
from ..program_id import PROGRAM_ID


class InitializePerpSyncQueueArgs(typing.TypedDict):
    nonce: int
    asset: types.asset.AssetKind


layout = borsh.CStruct("nonce" / borsh.U8, "asset" / types.asset.layout)


class InitializePerpSyncQueueAccounts(typing.TypedDict):
    admin: Pubkey
    zeta_program: Pubkey
    state: Pubkey
    perp_sync_queue: Pubkey
    pricing: Pubkey


def initialize_perp_sync_queue(
    args: InitializePerpSyncQueueArgs,
    accounts: InitializePerpSyncQueueAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["perp_sync_queue"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\n7\x9a\xe0\x81\xae\xa1\x08"
    encoded_args = layout.build(
        {
            "nonce": args["nonce"],
            "asset": args["asset"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
