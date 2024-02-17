from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateTickSizeArgs(typing.TypedDict):
    asset: types.asset.AssetKind
    tick_size: int


layout = borsh.CStruct("asset" / types.asset.layout, "tick_size" / borsh.U32)


class UpdateTickSizeAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_tick_size(
    args: UpdateTickSizeArgs,
    accounts: UpdateTickSizeAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdez\x01\xdd{t\x8fn"
    encoded_args = layout.build(
        {
            "asset": args["asset"].to_encodable(),
            "tick_size": args["tick_size"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
