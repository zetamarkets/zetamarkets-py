from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateHaltStateArgs(typing.TypedDict):
    args: types.halt_state_args.HaltStateArgs


layout = borsh.CStruct("args" / types.halt_state_args.HaltStateArgs.layout)


class UpdateHaltStateAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_halt_state(
    args: UpdateHaltStateArgs,
    accounts: UpdateHaltStateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xd7-5\xa2\x95\x8a\x05?"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
