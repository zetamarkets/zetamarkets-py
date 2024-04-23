from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class UpdateTakeTriggerOrderFeePercentageArgs(typing.TypedDict):
    new_take_trigger_order_fee_percentage: int


layout = borsh.CStruct("new_take_trigger_order_fee_percentage" / borsh.U64)


class UpdateTakeTriggerOrderFeePercentageAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey


def update_take_trigger_order_fee_percentage(
    args: UpdateTakeTriggerOrderFeePercentageArgs,
    accounts: UpdateTakeTriggerOrderFeePercentageAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe3\xea\x9d\xf6\x80J\xe96"
    encoded_args = layout.build(
        {
            "new_take_trigger_order_fee_percentage": args["new_take_trigger_order_fee_percentage"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
