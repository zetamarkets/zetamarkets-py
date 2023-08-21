from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ExpireSeriesArgs(typing.TypedDict):
    settlement_nonce: int


layout = borsh.CStruct("settlement_nonce" / borsh.U8)


def expire_series(
    args: ExpireSeriesArgs,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = []
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"-\xa2ib,\x15\xab\x7f"
    encoded_args = layout.build(
        {
            "settlement_nonce": args["settlement_nonce"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
