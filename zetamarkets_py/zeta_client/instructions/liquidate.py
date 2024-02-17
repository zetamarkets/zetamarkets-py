from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class LiquidateArgs(typing.TypedDict):
    size: int


layout = borsh.CStruct("size" / borsh.U64)


class LiquidateAccounts(typing.TypedDict):
    state: Pubkey
    liquidator: Pubkey
    liquidator_margin_account: Pubkey
    greeks: Pubkey
    oracle: Pubkey
    oracle_backup_feed: Pubkey
    oracle_backup_program: Pubkey
    market: Pubkey
    zeta_group: Pubkey
    liquidated_margin_account: Pubkey


def liquidate(
    args: LiquidateArgs,
    accounts: LiquidateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["state"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["liquidator"], is_signer=True, is_writable=False),
        AccountMeta(
            pubkey=accounts["liquidator_margin_account"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["greeks"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_feed"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["oracle_backup_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["market"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["zeta_group"], is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["liquidated_margin_account"],
            is_signer=False,
            is_writable=True,
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xdf\xb3\xe2}0.'J"
    encoded_args = layout.build(
        {
            "size": args["size"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
