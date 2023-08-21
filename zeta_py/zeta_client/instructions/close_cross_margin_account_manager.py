from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class CloseCrossMarginAccountManagerAccounts(typing.TypedDict):
    cross_margin_account_manager: Pubkey
    authority: Pubkey


def close_cross_margin_account_manager(
    accounts: CloseCrossMarginAccountManagerAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["cross_margin_account_manager"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=True),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe8\xb6\xb6\x89VXv\xfc"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
