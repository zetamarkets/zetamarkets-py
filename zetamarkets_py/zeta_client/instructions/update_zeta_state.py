from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateZetaStateArgs(typing.TypedDict):
    args: types.update_state_args.UpdateStateArgs


layout = borsh.CStruct("args" / types.update_state_args.UpdateStateArgs.layout)


class UpdateZetaStateAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_zeta_state(
    args: UpdateZetaStateArgs,
    accounts: UpdateZetaStateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"h\xb6\x14\xbb\x03\xa4<\x03"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
