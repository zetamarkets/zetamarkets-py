from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class ForceCancelTriggerOrderArgs(typing.TypedDict):
    trigger_order_bit: int


layout = borsh.CStruct("trigger_order_bit" / borsh.U8)


class ForceCancelTriggerOrderAccounts(typing.TypedDict):
    state: Pubkey
    admin: Pubkey
    trigger_order: Pubkey
    margin_account: Pubkey


def force_cancel_trigger_order(
    args: ForceCancelTriggerOrderArgs,
    accounts: ForceCancelTriggerOrderAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["margin_account"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"x\xec\xd8\x1c\xc0O\xff\xbc"
    encoded_args = layout.build(
        {
            "trigger_order_bit": args["trigger_order_bit"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
