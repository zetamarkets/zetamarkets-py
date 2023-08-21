from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class OverrideExpiryArgs(typing.TypedDict):
    args: types.override_expiry_args.OverrideExpiryArgs


layout = borsh.CStruct("args" / types.override_expiry_args.OverrideExpiryArgs.layout)


class OverrideExpiryAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    zeta_group: Pubkey


def override_expiry(
    args: OverrideExpiryArgs,
    accounts: OverrideExpiryAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x81\xc5urlw\xcf\x88"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
