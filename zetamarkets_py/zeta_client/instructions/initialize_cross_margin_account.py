from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID

from ..program_id import PROGRAM_ID


class InitializeCrossMarginAccountArgs(typing.TypedDict):
    subaccount_index: int


layout = borsh.CStruct("subaccount_index" / borsh.U8)


class InitializeCrossMarginAccountAccounts(typing.TypedDict):
    cross_margin_account: Pubkey
    cross_margin_account_manager: Pubkey
    authority: Pubkey
    payer: Pubkey
    zeta_program: Pubkey


def initialize_cross_margin_account(
    args: InitializeCrossMarginAccountArgs,
    accounts: InitializeCrossMarginAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["cross_margin_account"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["cross_margin_account_manager"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["payer"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["zeta_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x1b\x1a\xe42\xd2\xd3\xcd^"
    encoded_args = layout.build(
        {
            "subaccount_index": args["subaccount_index"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
