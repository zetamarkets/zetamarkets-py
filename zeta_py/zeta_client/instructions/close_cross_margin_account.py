from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CloseCrossMarginAccountArgs(typing.TypedDict):
    subaccount_index: int


layout = borsh.CStruct("subaccount_index" / borsh.U8)


class CloseCrossMarginAccountAccounts(typing.TypedDict):
    cross_margin_account: Pubkey
    cross_margin_account_manager: Pubkey
    authority: Pubkey


def close_cross_margin_account(
    args: CloseCrossMarginAccountArgs,
    accounts: CloseCrossMarginAccountAccounts,
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
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xcb\xc4\xbb<\r\xaa\xbeE"
    encoded_args = layout.build(
        {
            "subaccount_index": args["subaccount_index"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
