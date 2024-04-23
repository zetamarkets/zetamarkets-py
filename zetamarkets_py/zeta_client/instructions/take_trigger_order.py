from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class TakeTriggerOrderArgs(typing.TypedDict):
    trigger_order_bit: int


layout = borsh.CStruct("trigger_order_bit" / borsh.U8)


class TakeTriggerOrderAccounts(typing.TypedDict):
    trigger_order: Pubkey
    state: Pubkey
    pricing: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey
    bids: Pubkey
    asks: Pubkey
    taker: Pubkey
    taker_margin_account: Pubkey
    order_margin_account: Pubkey


def take_trigger_order(
    args: TakeTriggerOrderArgs,
    accounts: TakeTriggerOrderAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["trigger_order"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["bids"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["asks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["taker"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["taker_margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["order_margin_account"], is_signer=False, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"k\xcf;\xe2\x19\x17\x1f\xa1"
    encoded_args = layout.build(
        {
            "trigger_order_bit": args["trigger_order_bit"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
