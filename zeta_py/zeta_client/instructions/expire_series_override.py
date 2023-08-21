from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class ExpireSeriesOverrideArgs(typing.TypedDict):
    args: types.expire_series_override_args.ExpireSeriesOverrideArgs


layout = borsh.CStruct("args" / types.expire_series_override_args.ExpireSeriesOverrideArgs.layout)


def expire_series_override(
    args: ExpireSeriesOverrideArgs,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = []
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b'h\x16"{V\xe0\x82F'
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
