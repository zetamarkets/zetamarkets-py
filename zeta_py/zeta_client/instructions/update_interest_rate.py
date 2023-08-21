from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from .. import types
from ..program_id import PROGRAM_ID


class UpdateInterestRateArgs(typing.TypedDict):
    args: types.update_interest_rate_args.UpdateInterestRateArgs


layout = borsh.CStruct("args" / types.update_interest_rate_args.UpdateInterestRateArgs.layout)


class UpdateInterestRateAccounts(typing.TypedDict):
    state: Pubkey
    greeks: Pubkey
    zeta_group: Pubkey
    admin: Pubkey


def update_interest_rate(
    args: UpdateInterestRateArgs,
    accounts: UpdateInterestRateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"K\x08\xff){;\x87\xee"
    encoded_args = layout.build(
        {
            "args": args["args"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
