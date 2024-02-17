from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CancelTriggerOrderV2Args(typing.TypedDict):
    trigger_order_bit: int


layout = borsh.CStruct("trigger_order_bit" / borsh.U8)


class CancelTriggerOrderV2Accounts(typing.TypedDict):
    authority: Pubkey
    trigger_order: Pubkey
    margin_account: Pubkey


def cancel_trigger_order_v2(
    args: CancelTriggerOrderV2Args,
    accounts: CancelTriggerOrderV2Accounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdfAC\x07\xbd\x03?\x8e"
    encoded_args = layout.build(
        {
            "trigger_order_bit": args["trigger_order_bit"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
