from __future__ import annotations

import typing

from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class MigrateToCrossMarginAccountAccounts(typing.TypedDict):
    cross_margin_account: Pubkey
    pricing: Pubkey
    authority: Pubkey


def migrate_to_cross_margin_account(
    accounts: MigrateToCrossMarginAccountAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["cross_margin_account"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["pricing"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["authority"], is_signer=True, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x9d5kh\xb8\xbdd\xdc"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
