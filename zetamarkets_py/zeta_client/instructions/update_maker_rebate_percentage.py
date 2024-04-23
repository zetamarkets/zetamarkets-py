from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class UpdateMakerRebatePercentageArgs(typing.TypedDict):
    native_maker_rebate_percentage: int


layout = borsh.CStruct("native_maker_rebate_percentage" / borsh.U64)


class UpdateMakerRebatePercentageAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_maker_rebate_percentage(
    args: UpdateMakerRebatePercentageArgs,
    accounts: UpdateMakerRebatePercentageAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xb4\xec\xfd\x13\xe7\xe7\xdcA"
    encoded_args = layout.build(
        {
            "native_maker_rebate_percentage": args["native_maker_rebate_percentage"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
